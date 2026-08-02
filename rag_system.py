# rag_system.py
# sections when a user asks a question.

import os
import numpy as np
from sentence_transformers import SentenceTransformer

# Use absolute path so it works no matter where the app is started from
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "resume", "Data.md")


def load_and_chunk_documents():
    """Read Data.md and split it into chunks using '## ' headings."""
    try:
        with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print("[RAG ERROR] resume/Data.md not found.")
        return ["Error: resume/Data.md not found."]

    parts = text.split("\n## ")
    chunks = []
    for i, part in enumerate(parts):
        part = part.strip()
        if part:
            # add back the "## " heading marker except for the first chunk
            prefix = "## " if i > 0 else ""
            chunks.append(prefix + part)

    print(f"[RAG] Loaded {len(chunks)} chunks from Data.md")
    return chunks


# Load model and data once when the app starts
print("[RAG] Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

all_chunks = load_and_chunk_documents()
chunk_embeddings = model.encode(all_chunks)
print("[RAG] Ready.")


def find_matching_resume_sections(user_query, top_n=3):
    """Find the top_n chunks most relevant to the user's question."""
    try:
        query_embedding = model.encode([user_query])[0]

        # cosine similarity between query and every chunk
        scores = np.dot(chunk_embeddings, query_embedding) / (
            np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )

        # small keyword boost so obvious matches rank higher
        query_lower = user_query.lower()
        keywords = ["project", "experience", "skill"]
        for i, chunk in enumerate(all_chunks):
            heading = chunk.split("\n")[0].lower()
            for word in keywords:
                if word in query_lower and word in heading:
                    scores[i] += 1.0
            if ("college" in query_lower or "education" in query_lower) and "education" in heading:
                scores[i] += 1.0

        # get indexes of the top scoring chunks
        top_indexes = np.argsort(scores)[::-1][:top_n]

        best_chunks = [all_chunks[i] for i in top_indexes]
        return "\n\n---\n\n".join(best_chunks)

    except Exception as error:
        print(f"[RAG ERROR] {error}")
        return "Error: Unable to process data retrieval."
