import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}&pageSize=5"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    
    # Create an empty list to collect our formatted text blocks
    collected_results = []
    
    for article in articles:
        # Build a neat string for each article
        article_summary = (
            f"Title: {article['title']}\n"
            f"Source: {article['source']['name']}\n"
            f"URL: {article['url']}\n"
            f"---"
        )
        # Add it to our pile
        collected_results.append(article_summary)
        
    # Join all the summaries together with newlines and return them to the AI
    return "\n".join(collected_results)
