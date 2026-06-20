import requests
import os
from dotenv import load_dotenv
from database import save_article

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(topic):
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

        # Save this article permanently to the PostgreSQL database
        save_article(title, source, link, published_at, content)

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

if __name__ == "__main__":
    fetch_news("Artificial Intelligence")