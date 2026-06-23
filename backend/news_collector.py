import requests
import os
from dotenv import load_dotenv
from vector_store import add_article
from embeddings import get_embedding
from database import save_article,get_cached_articles

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(topic):
    # Checking the database before making the API call
    cached_data = get_cached_articles(topic, hours_limit=24)

    if cached_data and len(cached_data) > 0:
        print(f"✅ Found {len(cached_data)} recent articles in the local database! Skipping API call.")
        
        collected_results = []
        # cached_data is a list of tuples: (title, source, url, published_at, content)
        for row in cached_data:
            title, source, url, published_at, content = row
            article_summary = (
                f"Title: {title}\n"
                f"Source: {source}\n"
                f"URL: {url}\n"
                f"---"
            )
            collected_results.append(article_summary)
            
        return "\n".join(collected_results)

    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}&pageSize=5"
    response = requests.get(url)
    articles = response.json().get("articles", [])

    # Create an empty list to collect our formatted text blocks
    collected_results = []

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

        text = f"{title}\n{content or ""}"

        embedding = get_embedding(text)

        add_article(article_id,embedding)

        # Build a neat string for each article (for Gemini to read)
        article_summary = (
            f"Title: {title}\n"
            f"Source: {source}\n"
            f"URL: {link}\n"
            f"---"
        )
        collected_results.append(article_summary)

    print(f"Saved {len(articles)} articles to the database!")

    # Join all the summaries together with newlines and return them to the AI
    return "\n".join(collected_results)
