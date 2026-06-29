from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import create_agent
from embeddings import get_embedding
from vector_store import initialize_index
from retrieval import retrieve_relevant_articles, context_builder
from news_collector import fetch_news


load_dotenv()


print("⚙️ Assembling the Gemini News Agent architecture...")
# Gemini automatically looks into the system memory for "GOOGLE_API_KEY"
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
print("🤖 Agent is active and standing by!")


def run_news_agent(user_question, chat_history=None):
    if chat_history == None:
        chat_history = []
    
    articles = retrieve_relevant_articles(user_question)
    context = context_builder(articles)

    print(f"DEBUG: context length = {len(context.strip())}")  # add this
    print(f"DEBUG: context preview = {context[:200]}")        # add this


    if not articles or not context or len(context.strip()) < 100:
        print("No relevant articles found locally, fetching news....")
        fetch_news(user_question)
        articles = retrieve_relevant_articles(user_question)
        context = context_builder(articles)
        print(f"DEBUG: context after fetch = {len(context.strip())}")  # add this
        print(f"DEBUG: articles after fetch = {len(articles)}")
        
    prompt = f"""
    Answer the following question using ONLY the context below.
    If the context doesn't contain a relevant answer, say "I don't have enough verified data."
    Never use your own knowledge.

    Context:
    {context}

    Question: {user_question}
    """

    chat_history.append(HumanMessage(content = prompt))
    response = llm.invoke(chat_history)
    clean_text = response.content
    chat_history.append(AIMessage(content = clean_text))


    return clean_text, chat_history

