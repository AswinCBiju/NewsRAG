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
    cached_data = get_cached_articles(topic, hours_limit=24)

    if cached_data and len(cached_data) > 0:
        print(f"✅ Found {len(cached_data)} cached articles, loading into FAISS...")
        for row in cached_data:
            article_id, title, source, url, published_at, content = row
            text = f"{title}\n{content or ''}"
            embedding = get_embedding(text)
            add_article(article_id, embedding)
        return f"Loaded {len(cached_data)} cached articles into context."

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
    articles = [a for a in articles if a.get("title") and a.get("publishedAt") and a.get("url")]

    for article in articles:
        title = article["title"]
        source = article["source"]["name"]
        link = article["url"]
        published_at = article["publishedAt"]
        content = article.get("content", "")

        print(f"Title: {title}\nSource: {source}\nURL: {link}\n---")

        article_id = save_article(title, source, link, published_at, content)
        text = f"{title}\n{content or ''}"
        embedding = get_embedding(text)
        add_article(article_id, embedding)

    print(f"Saved {len(articles)} articles to the database!")
    return f"Fetched and indexed {len(articles)} fresh articles. Now use retrieve_news_context to answer."
