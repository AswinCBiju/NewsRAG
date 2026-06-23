import requests
import os
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
from vector_store import add_article
from embeddings import get_embedding
from database import save_article,get_cached_articles

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def fetch_news(topic):
    # Checking the database before making the API call
    cached_data = get_cached_articles(topic, hours_limit=24)

    if cached_data and len(cached_data) > 0:
        print(f"✅ Found {len(cached_data)} recent articles in the local database! Skipping API call.")
        
        scored_articles = []
        # cached_data is a list of tuples: (title, source, url, published_at, content)
        query_embedding = get_embedding(topic)

        for row in cached_data:
            article_id,title, source, url, published_at, content = row
            
            text = f"{title}\n{content or ''}"
            embedding = get_embedding(text)
            
            score = cosine_similarity(query_embedding,embedding)
            scored_articles.append((score, title, source, url, embedding))
        
        scored_articles.sort(reverse=True, key=lambda x: x[0])
        # keep only relevant ones
        scored_articles = [x for x in scored_articles if x[0] > 0.35]

        return "\n".join(
            f"Title: {title}\nSource: {source}\nURL: {url}\n---"
            for score, title, source, url, embedding in scored_articles[:5]
        )

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
    query_embedding = get_embedding(topic)

    def is_valid(article):
        return (
            article.get("title")
            and article.get("publishedAt")
            and article.get("url")
        )

    articles = [a for a in articles if is_valid(a)]

    # Create an empty list to collect our formatted text blocks
    scored_articles = []
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

        # Save this article permanently to the PostgreSQL database while also converting them into embeddings so FAISS can store them as vector embeddings
        article_id = save_article(title, source, link, published_at, content)

        text = f"{title}\n{content or ''}"

        embedding = get_embedding(text)

        score = cosine_similarity(query_embedding,embedding)
        scored_articles.append((score, title, source, link, embedding))
        
        add_article(article_id,embedding)
    
    scored_articles.sort(reverse=True, key=lambda x: x[0])
    # keep only relevant ones
    scored_articles = [x for x in scored_articles if x[0] > 0.35]

    print(f"Saved {len(articles)} articles to the database!")

    # Join all the summaries together with newlines and return them to the AI
    return "\n".join(
        f"Title: {title}\nSource: {source}\nURL: {url}\n---"
        for score, title, source, url, embedding in scored_articles[:5]
    )
