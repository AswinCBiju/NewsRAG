from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchResults
from langchain.agents import create_agent

load_dotenv()

print("⚙️ Assembling the Gemini News Agent architecture...")
# Gemini automatically looks into the system memory for "GOOGLE_API_KEY"
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

# 2. Build the tool list
search_tool = DuckDuckGoSearchResults(backend="news", max_results=3)
tools = [search_tool]

# 2. In the new version, you pass the prompt and tools directly into create_agent.
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
    
    # Extracting output from the modern agent state response structure
    return response["messages"][-1].content[0]["text"]

if __name__ == "__main__":
    # Test message 1 (Reuses the global agent)
    print(run_news_agent("What is the latest news about OpenAI?"))
    
    # Test message 2 (Instantly fires because the agent is already built!)
    print(run_news_agent("What is the latest news about NASA?"))



