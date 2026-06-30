from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

from retrieval import retrieve_relevant_articles, context_builder
from news_collector import fetch_news

load_dotenv()

print("⚙️ Assembling the Gemini News Agent architecture...")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)

print("🤖 Agent is active and standing by!")


def run_news_agent(user_question, chat_history=None):
    if chat_history is None:
        chat_history = []

    print(f"\n🔍 User question: {user_question}")

    # Always fetch fresh news for the current query
    print("📰 Fetching latest news from NewsAPI...")
    fetch_news(user_question)

    # Retrieve relevant articles after indexing
    articles = retrieve_relevant_articles(user_question)
    context = context_builder(articles)

    print(f"DEBUG: articles retrieved = {len(articles)}")
    print(f"DEBUG: context length = {len(context.strip())}")
    print(f"DEBUG: context preview = {context[:200]}")

    # If retrieval failed
    if not articles or len(context.strip()) == 0:
        return (
            "I couldn't find any relevant news articles for that topic.",
            chat_history
        )

    prompt = f"""
You are a news assistant.

Answer the user's question using ONLY the news context below.

Rules:
- Never use your own knowledge.
- Never make assumptions.
- If the context is insufficient, respond with:
  "I don't have enough verified data."
- Summarize the information clearly and naturally.

Context:
{context}

Question:
{user_question}
"""

    chat_history.append(HumanMessage(content=prompt))

    try:
        response = llm.invoke(chat_history)
        clean_text = response.content

    except Exception as e:
        print(f"Gemini Error: {e}")

        clean_text = (
            "Gemini API quota has been exhausted or the service is temporarily "
            "unavailable. Please wait a minute and try again."
        )

    chat_history.append(AIMessage(content=clean_text))

    return clean_text, chat_history