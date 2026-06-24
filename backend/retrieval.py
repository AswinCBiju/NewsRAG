from embeddings import get_embedding
from vector_store import search_articles
from database import get_articles_by_ids

def retrieve_relevant_articles(query):
    query_embedding =  get_embedding(query)
    ids = search_articles(query_embedding)
    articles = get_articles_by_ids(ids)
    return articles

def context_builder(articles):
    context = ""

    for article in articles:
        _, title, source, url, content = article

        context += f"""
            Title: {title}
            Source: {source}

            Content:
            {content}

            ---
        """

    return context