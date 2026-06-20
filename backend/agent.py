from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from news_collector import fetch_news

load_dotenv()

print("⚙️ Assembling the Gemini News Agent architecture...")
# Gemini automatically looks into the system memory for "GOOGLE_API_KEY"
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
# Adding the news_collector function into the tools list using the tool decorator
@tool
def fetch_news_gemini(topic: str) -> str:
    """Use this tool to fetch live news articles, publisher sources, and links about a specific topic."""
    return fetch_news(topic)

# Build the tool list
tools = [fetch_news_gemini]

# In the new version, you pass the prompt and tools directly into create_agent.
# No need to manually build an AgentExecutor!
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a professional, real-time news analyst. Look up the latest information using your search tool before answering. Always cite the headlines or sources you use."
)

print("🤖 Agent is active and standing by!")


def run_news_agent(user_question):
    # Fix: Modern LangChain agents expect a dictionary containing a query structure
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": user_question}
        ]
    })
    
    # Grab the final message object from the agent
    final_message = response["messages"][-1]
    content = final_message.content

    # Case A: If content is already a plain string, return it directly!
    if isinstance(content, str):
        return content
        
    # Case B: If content is a list of blocks (with metadata), extract the text safely
    if isinstance(content, list) and len(content) > 0:
        first_block = content[0]
        if isinstance(first_block, dict) and "text" in first_block:
            return first_block["text"]
            
    # Fallback just in case something completely weird comes back
    return str(content)

if __name__ == "__main__":
    print("\n🖥️ Local CLI Testing Mode Active (Type 'exit' to quit)")
    print("=" * 50)

    while True:
        user_prompt = input("Ask the agent a question: ")
        if user_prompt.lower() == "exit":
            print("Goodbye !!\n")
            break
        
        print("\nSearching and analyzing...")
        try:
            result = run_news_agent(user_prompt)
            print(f"\nResponse:\n{result}")
        except Exception as e:
            print(f"An error occurred: {e}")



