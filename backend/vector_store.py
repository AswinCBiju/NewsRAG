import faiss
from database import get_connection
from embeddings import get_embedding
import numpy as np

DIMENSION = 384

index = faiss.IndexFlatL2(DIMENSION)

article_ids = []

def initialize_index():
    """On startup, re-embed all articles from DB into FAISS."""
    print("🔄 Re-indexing articles from database into FAISS...")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, content FROM articles ORDER BY saved_at DESC LIMIT 100")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    for article_id, title, content in rows:
        text = f"{title}\n{content or ''}"
        embedding = get_embedding(text)
        add_article(article_id, embedding)

    print(f"✅ FAISS re-indexed with {len(article_ids)} articles.")

def add_article(article_id, embedding):
    embedding = np.array(embedding, dtype="float32").reshape(1,-1)

    index.add(embedding)
    article_ids.append(article_id)

    print(f"Indexed articles: {len(article_ids)}")

def search_articles(query_embedding, k=5):
    query_embedding = np.array(query_embedding, dtype="float32").reshape(1,-1)

    distances, indices = index.search(query_embedding, k)

    return [
        article_ids[i]
        for i in indices[0]
        if i != -1 and
        i < len(article_ids)
    ]