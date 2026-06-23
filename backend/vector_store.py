import faiss
import numpy as np

DIMENSION = 384

index = faiss.IndexFlatL2(DIMENSION)

article_ids = []

def add_article(article_id, embedding):
    embedding = np.array([embedding], dtype="float32")
    index.add(embedding)
    article_ids.append(article_id)
    print(f"Indexed articles: {len(article_ids)}")

def search(query_embedding, k=5):
    query_embedding = np.array([query_embedding], dtype="float32")

    distances, indices = index.search(query_embedding, k)

    return [
        article_ids[i]
        for i in indices[0]
        if i != -1
    ]