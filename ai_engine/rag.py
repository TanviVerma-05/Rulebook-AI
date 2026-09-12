import sys
import os
import json
from pathlib import Path
from unittest import result

import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google import genai
from google.genai import types

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


# ==================================================
# PATHS
# ==================================================

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"

EMBEDDINGS_FILE = DATA_DIR / "embeddings.npy"
METADATA_FILE = DATA_DIR / "metadata.json"


# ==================================================
# CONFIGURATION
# ==================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GENERATION_MODEL = "gemini-3.5-flash-lite"

TOP_K = 6
MIN_RELEVANCE_SCORE = 0.50


# ==================================================
# LOAD ENVIRONMENT
# ==================================================

load_dotenv(ROOT / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )


# ==================================================
# INITIALIZE MODELS
# ==================================================

print("Loading embedding model...", file=__import__("sys").stderr)

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

client = genai.Client(
    api_key=API_KEY
)


# ==================================================
# LOAD INDEX
# ==================================================

if not EMBEDDINGS_FILE.exists():
    raise FileNotFoundError(
        "embeddings.npy not found. Run embeddings.py first."
    )

if not METADATA_FILE.exists():
    raise FileNotFoundError(
        "metadata.json not found. Run embeddings.py first."
    )


embeddings = np.load(
    EMBEDDINGS_FILE
)

with open(
    METADATA_FILE,
    "r",
    encoding="utf-8"
) as f:

    metadata = json.load(f)

# ==================================================
# SEMANTIC SEARCH
# ==================================================


def search(query, top_k=TOP_K):

    query_embedding = embedding_model.encode(
        [query],
        normalize_embeddings=True
    )[0]

    # Because both vectors are normalized,
    # dot product = cosine similarity.

    scores = embeddings @ query_embedding

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in top_indices:

        document = metadata[int(index)].copy()

        document["score"] = float(
            scores[int(index)]
        )

        results.append(document)

    return results

# ==================================================
# BUILD EVIDENCE
# ==================================================


def build_evidence(results):

    evidence = []

    for i, result in enumerate(results, start=1):

        page = result.get("page")

        page_text = (
            f"Page: {page}"
            if page is not None
            else "Page: N/A"
        )

        evidence.append(
            f"""
            EVIDENCE {i}
            Chunk ID: {result["chunk_id"]}
            Source: {result["source"]}
            Section: {result["section"]}
            {page_text}
            Similarity: {result["score"]:.4f}

            TEXT:
                {result["text"]}
                """
        )

    return "\n".join(evidence)

# ==================================================
# GROUNDED ANSWER
# ==================================================


def generate_answer(question, results):

    evidence = build_evidence(results)

    prompt = f"""
    You are the grounded question-answering engine for a
    university rulebook.

    IMPORTANT RULES:

        1. Use ONLY the evidence supplied below.
        2. Do NOT use your general knowledge.
        3. Do NOT invent policies, dates, numbers, rules, or exceptions.
        4. If the evidence does not contain enough information
        to answer the question, return NO_EVIDENCE.
        5. If two pieces of evidence give materially incompatible
        answers to the same question, return CONTRADICTION.
        6. If the evidence supports one clear answer, return ANSWER.
        7. Every factual claim in an ANSWER must have a citation.
        8. Citations must refer ONLY to the supplied evidence.
        9. Quotes must be copied from the evidence exactly.
        10. Keep the answer concise and useful for a student.

        The possible states are:

            ANSWER
            NO_EVIDENCE
            CONTRADICTION

            Return ONLY valid JSON using this exact structure:

                {{
                    "state": "ANSWER",
                    "answer": "short answer",
                    "citations": [
                        {{
                            "chunk_id": "chunk id",
                            "source": "source filename",
                            "section": "section",
                            "page": null,
                            "quote": "exact supporting quote"
                        }}
                    ],
                    "conflicts": []
                }}

                For NO_EVIDENCE:

                    {{
                        "state": "NO_EVIDENCE",
                        "answer": "The rulebook does not provide enough evidence to answer this question.",
                        "citations": [],
                        "conflicts": []
                    }}

                    For CONTRADICTION:

                        {{
                            "state": "CONTRADICTION",
                            "answer": "The supplied rulebook contains conflicting information.",
                            "citations": [],
                            "conflicts": [
                                {{
                                    "chunk_id": "chunk id",
                                    "source": "source filename",
                                    "section": "section",
                                    "page": null,
                                    "claim": "conflicting claim"
                                }}
                            ]
                        }}

                        QUESTION:
                        {question}

                        SUPPLIED EVIDENCE:
                        {evidence}
                        """

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.0
        )
    )

    text = response.text.strip()

    try:
        result = json.loads(text)

    except json.JSONDecodeError:

        return {
            "state": "NO_EVIDENCE",
            "answer": "The system could not produce a valid grounded response.",
            "citations": [],
            "conflicts": []
        }

    return result


# ==================================================
# MAIN ASK FUNCTION
# ==================================================

def ask(question):
    question = question.strip()

    if not question:
        return {
            "state": "NO_EVIDENCE",
            "answer": "Please enter a question.",
            "citations": [],
            "conflicts": []
        }


    results = search(question, TOP_K)

    # If the best retrieved evidence is not relevant enough,
    # refuse without calling the LLM.
    if not results or results[0]["score"] < MIN_RELEVANCE_SCORE:
        return {
            "state": "NO_EVIDENCE",
            "answer": (
                "The rulebook does not provide enough evidence "
                "to answer this question."
            ),
            "citations": [],
            "conflicts": []
        }

    # Only use Gemini when relevant evidence exists.
    answer = generate_answer(question, results)

    answer["retrieved"] = [
        {
            "chunk_id": r["chunk_id"],
            "source": r["source"],
            "section": r["section"],
            "page": r["page"],
            "score": r["score"]
        }
        for r in results
    ]

    return answer


# ==================================================
# COMMAND LINE TEST
# ==================================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--question",
        type=str,
        required=True
    )

    args = parser.parse_args()

    result = ask(args.question)

    print(
        json.dumps(
            result,
            ensure_ascii=False
        )
    )
