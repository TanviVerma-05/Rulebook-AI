from pathlib import Path
from pypdf import PdfReader


CHUNK_SIZE = 900
OVERLAP = 150


def chunk_text(text):
    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0
    step = CHUNK_SIZE - OVERLAP

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += step

    return chunks


def find_section(text, position):
    before = text[:position]
    lines = before.splitlines()

    section = "General"

    for line in lines:
        line = line.strip()

        if line.startswith("#"):
            section = line.lstrip("#").strip()

    return section


def load_markdown_file(file_path):

    path = Path(file_path)

    print("    Reading:", path)

    text = path.read_text(encoding="utf-8")

    print("    Characters:", len(text))

    documents = []

    start = 0
    chunk_number = 1
    step = CHUNK_SIZE - OVERLAP

    while start < len(text):

        end = start + CHUNK_SIZE

        chunk = text[start:end].strip()

        if chunk:

            documents.append({
                "chunk_id": f"{path.stem}_{chunk_number}",
                "text": chunk,
                "source": path.name,
                "section": find_section(text, start),
                "page": None
            })

            chunk_number += 1

        start += step

    return documents


def load_pdf_file(file_path):

    path = Path(file_path)

    reader = PdfReader(str(path))

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):

            documents.append({
                "chunk_id": f"{path.stem}_p{page_number}_{i + 1}",
                "text": chunk,
                "source": path.name,
                "section": f"PDF Page {page_number}",
                "page": page_number
            })

    return documents


def load_corpus(corpus_dir):

    corpus_path = Path(corpus_dir)

    print("CORPUS PATH:", corpus_path)
    print("FILES FOUND:", [f.name for f in corpus_path.iterdir()])
    print()

    documents = []

    for file_path in sorted(corpus_path.iterdir()):

        if not file_path.is_file():
            continue

        print("Checking:", file_path.name)

        suffix = file_path.suffix.lower()

        if suffix in [".md", ".txt"]:

            print("Loading Markdown/Text:", file_path.name)

            loaded = load_markdown_file(file_path)

            print("  ->", len(loaded), "chunks")

            documents.extend(loaded)

        elif suffix == ".pdf":

            print("Loading PDF:", file_path.name)

            loaded = load_pdf_file(file_path)

            print("  ->", len(loaded), "chunks")

            documents.extend(loaded)

    return documents


if __name__ == "__main__":

    corpus_dir = Path(__file__).resolve().parents[1] / "corpus"

    documents = load_corpus(corpus_dir)

    print(f"\nLoaded {len(documents)} chunks.")

    print("\nFirst 5 chunks:")

    for document in documents[:5]:

        print("\n---")
        print("ID:", document["chunk_id"])
        print("Source:", document["source"])
        print("Section:", document["section"])
        print("Page:", document["page"])
        print("Text:", document["text"][:250])
