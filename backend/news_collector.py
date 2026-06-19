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

        save_article(title, source, link, published_at, content)

    print(f"Saved {len(articles)} articles to the database!")

if __name__ == "__main__":
    fetch_news("Artificial Intelligence")
    