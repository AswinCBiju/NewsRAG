import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}&pageSize=5"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    
    for article in articles:
        print("Title:", article["title"])
        print("Source:", article["source"]["name"])
        print("URL:", article["url"])
        print("---")

if __name__ == "__main__":
    fetch_news("Artificial Intelligence")
    