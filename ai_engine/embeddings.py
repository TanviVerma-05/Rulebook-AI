from pathlib import Path
import json

import numpy as np
from sentence_transformers import SentenceTransformer

from documents import load_corpus


# --------------------------------------------------
# Paths
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

CORPUS_DIR = ROOT / "corpus"
DATA_DIR = ROOT / "data"

DATA_DIR.mkdir(exist_ok=True)

EMBEDDINGS_FILE = DATA_DIR / "embeddings.npy"
METADATA_FILE = DATA_DIR / "metadata.json"


# --------------------------------------------------
# Local embedding model
# --------------------------------------------------

MODEL_NAME = "all-MiniLM-L6-v2"

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded.")


# --------------------------------------------------
# Generate embeddings
# --------------------------------------------------

def generate_embeddings(documents):

    texts = [
        document["text"]
        for document in documents
    ]

    print(f"\nGenerating embeddings for {len(texts)} chunks...")

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    return np.array(
        embeddings,
        dtype=np.float32
    )

    # --------------------------------------------------
    # Main
    # --------------------------------------------------


if __name__ == "__main__":

    print("\nLoading corpus...")

    documents = load_corpus(CORPUS_DIR)

    print(f"\nTotal chunks: {len(documents)}")

    if not documents:
        raise ValueError("No documents found.")

    embeddings = generate_embeddings(documents)

    print("\nEmbedding shape:", embeddings.shape)

    # Save embeddings
    np.save(
        EMBEDDINGS_FILE,
        embeddings
    )

    # Save metadata
    with open(
        METADATA_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            documents,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("\nSaved:")
    print(" -", EMBEDDINGS_FILE)
    print(" -", METADATA_FILE)

    print("\nEmbedding generation complete!")
