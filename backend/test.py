from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests
import os


load_dotenv()


NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def article(topic):
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
    print(response.status_code)
    print(response.text)
    articles = response.json().get("articles", [])

    return articles

articles = article("Steam machine")
print(articles)