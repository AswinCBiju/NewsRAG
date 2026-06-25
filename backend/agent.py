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

initialize_index()

print("⚙️ Assembling the Gemini News Agent architecture...")
# Gemini automatically looks into the system memory for "GOOGLE_API_KEY"
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
# Adding the news_collector function into the tools list using the tool decorator
@tool
def fetch_news_gemini(topic: str) -> str:
    """
    Use this tool to fetch and index fresh news articles about a topic.
    Only call this if retrieve_news_context returned no useful results.
    After calling this, always follow up with retrieve_news_context.
    """
    return fetch_news(topic)

@tool
def retrieve_news_context(query: str) -> str:
    """
    Use this tool FIRST for every question.
    Searches the local knowledge base for relevant articles.
    Returns article content to answer the user's question.
    """

    articles = retrieve_relevant_articles(query)
    context = context_builder(articles)

    return context


# Build the tool list
tools = [
    fetch_news_gemini,
    retrieve_news_context
]

# In the new version, you pass the prompt and tools directly into create_agent.
# No need to manually build an AgentExecutor!
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=
    """
    You are a strict news QA system with a two-step process.

    ALWAYS follow this exact order:
    1. ALWAYS call retrieve_news_context first for every question.
    2. If the context contains a relevant answer, respond using only that information.
    3. If retrieve_news_context returns empty or irrelevant results, THEN call fetch_news_gemini to fetch fresh articles.
    4. After fetch_news_gemini, ALWAYS call retrieve_news_context again to get the actual content.
    5. Never answer from memory or training data.
    6. If no tool result is useful, say "I don't have enough verified data."
    """
)

print("🤖 Agent is active and standing by!")


def run_news_agent(user_question, chat_history=None):
    if chat_history == None:
        chat_history = []
    
    # Adding the user query to the chat history
    chat_history.append(HumanMessage(content=user_question))

    # Feed the ENTIRE running history conversation to the agent
    response = agent.invoke({
        "messages": chat_history
    })
    
    # Grab the final message object from the agent
    final_message = response["messages"][-1]
    content = final_message.content

    clean_text = ""

    # Case A: If content is already a plain string, return it directly!
    if isinstance(content, str):
        clean_text =  content
        
    # Case B: If content is a list of blocks (with metadata), extract the text safely
    elif isinstance(content, list) and len(content) > 0:
        first_block = content[0]
        if isinstance(first_block, dict) and "text" in first_block:
            clean_text = first_block["text"]
            
    else:
        clean_text = str(content)

    chat_history.append(AIMessage(content=clean_text))


    return clean_text,chat_history

if __name__ == "__main__":
    print("\n🖥️ Local CLI Testing Mode Active (Type 'exit' to quit)")
    print("=" * 50)

    session_history = []
    while True:
        user_prompt = input("Ask the agent a question: ")
        if user_prompt.lower() == "exit":
            print("Goodbye !!\n")
            break
        print("\nSearching and analyzing...")
        try:
            result,session_history = run_news_agent(user_prompt,session_history)
            print(f"\nResponse:\n{result}")
        except Exception as e:
            print(f"An error occurred: {e}")



