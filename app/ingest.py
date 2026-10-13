import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb


# Load the embedding model once at module level
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("documents")


def load_documents(folder_path: str) -> list[dict]:
    """Load all PDFs and text files from a folder."""
    docs = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if filename.endswith(".pdf"):
            reader = PdfReader(filepath)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            docs.append({"source": filename, "text": text})
        elif filename.endswith(".txt") or filename.endswith(".md"):
            with open(filepath, "r", encoding="utf-8") as f:
                docs.append({"source": filename, "text": f.read()})
    return docs


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    """Split text into small overlapping chunks, respecting paragraph boundaries."""
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    for para in paragraphs:
        # Hard-split any paragraph that's already too big
        if len(para) > chunk_size:
            if current:
                chunks.append(current.strip())
                current = ""
            for i in range(0, len(para), chunk_size - overlap):
                chunks.append(para[i:i + chunk_size].strip())
            continue
        if len(current) + len(para) <= chunk_size:
            current += para + "\n\n"
        else:
            if current:
                chunks.append(current.strip())
            current = para + "\n\n"
    if current:
        chunks.append(current.strip())
    return [c for c in chunks if c]


def ingest(folder_path: str):
    """Load documents, chunk them, embed them, and store in ChromaDB."""
    docs = load_documents(folder_path)
    if not docs:
        print(f"No documents found in {folder_path}")
        return

    for doc in docs:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
            embedding = model.encode(chunk).tolist()
            collection.add(
                ids=[f"{doc['source']}_{i}"],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source": doc["source"], "chunk_index": i}],
            )
    print(f"Ingested {collection.count()} chunks from {len(docs)} document(s)")


if __name__ == "__main__":
    ingest("data/sample_docs")