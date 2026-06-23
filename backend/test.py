from retrieval import retrieve_relevant_articles, context_builder
from news_collector import fetch_news

fetch_news("gta 6")
articles = retrieve_relevant_articles("whats hot on gta 6")
context = context_builder(articles)


print(context)