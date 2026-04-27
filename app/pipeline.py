import json

def load_reviews(path="../data/raw_reviews.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def chunk_reviews(reviews, chunk_size=200):
    chunks = []

    for r in reviews:
        text = r["text"]
        for i in range(0, len(text), chunk_size):
            chunks.append({
                "review_id": r["review_id"],
                "product": r["product"],
                "text": text[i:i+chunk_size],
                "language": r["language"]
            })

    return chunks

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def create_vector_store(chunks):
    texts = [c["text"] for c in chunks]

    embeddings = model.encode(texts, show_progress_bar=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index, chunks, embeddings

def retrieve_reviews(query, index, chunks, top_k=5):
    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), top_k)

    results = []
    for idx in indices[0]:
        results.append(chunks[idx])

    return results

def filter_by_product(chunks, product_name):
    return [c for c in chunks if c["product"] == product_name]

if __name__ == "__main__":
    reviews = load_reviews()
    chunks = chunk_reviews(reviews)

    index, chunks, embeddings = create_vector_store(chunks)

    query = "Is this stroller good quality for babies?"
    results = retrieve_reviews(query, index, chunks)

    print("\nRetrieved Reviews:\n")
    for r in results:
        print(r["text"])