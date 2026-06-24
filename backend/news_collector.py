import requests
import faiss
import os
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
from vector_store import add_article, index, article_ids
from embeddings import get_embedding
from database import save_article,get_cached_articles,get_articles_by_ids

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(topic):
    # Checking the database before making the API call
    cached_data = get_cached_articles(topic, hours_limit=24)

    if cached_data and len(cached_data) > 0:
        print(f"✅ Found {len(cached_data)} recent articles in the local database! Skipping API call.")
        for row in cached_data:
            article_id, title, source, url, published_at, content = row
            text = f"{title}\n{content or ''}"
            embedding = get_embedding(text)
            add_article(article_id, embedding)
    else:
        # =========================
        # FETCH FROM NEWS API
        # =========================
        from_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")

        url = (
            "https://newsapi.org/v2/everything?"
            f"q={topic}&"
            f"from={from_date}&"
            "sortBy=publishedAt&"
            "language=en&"
            f"pageSize=10&"
            f"apiKey={NEWS_API_KEY}"
        )

        response = requests.get(url)
        articles = response.json().get("articles", [])

        def is_valid(article):
            return (
                article.get("title")
                and article.get("publishedAt")
                and article.get("url")
            )

        articles = [a for a in articles if is_valid(a)]

        for article in articles:
            title = article["title"]
            source = article["source"]["name"]
            link = article["url"]
            published_at = article["publishedAt"]
            content = article.get("content", "")

            print("Title:", title)
            print("Source:", source)
            print("URL:", link)
            print("---")

            # Save to DB
            article_id = save_article(title, source, link, published_at, content)

            # Embed + store in FAISS
            text = f"{title}\n{content or ''}"
            embedding = get_embedding(text)

            add_article(article_id, embedding)

        print(f"Saved {len(articles)} articles to the database!")


    query_embedding = get_embedding(topic)
    query_vector = np.array(query_embedding, dtype="float32").reshape(1, -1)

    distances, indices = index.search(query_vector,5)

    top_article_ids = [
        article_ids[i]
        for i in indices[0]
        if i != -1 and i < len(article_ids)
    ]

    results = []
    for article_id in top_article_ids:
        rows = get_articles_by_ids(article_id)
        if rows:
            results.append(rows[0])

    return "\n".join(
        f"Title: {r[1]}\nSource: {r[2]}\nURL: {r[3]}\n---"
        for r in results
    )
