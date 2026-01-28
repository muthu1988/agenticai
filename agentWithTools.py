from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

# 1. Define the Tools (using langchain_core for consistency)
@tool
def calculator(expression: str) -> str:
    """Useful for when you need to answer questions about math."""
    try:
        # Note: eval is used here for the example; use a safer parser in production
        return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"

tools = [calculator]

# 2. Setup the LLM (Phi-3)
# Ensure you have ollama run phi3 working locally
model = ChatOllama(model="qwen2.5", temperature=0)

# 3. Construct the Agent
# LangGraph's prebuilt agent handles the prompt and loop logic automatically
agent_executor = create_react_agent(model, tools)

# 4. Run the Agent
# LangGraph agents expect a list of messages rather than "input" strings
inputs = {"messages": [HumanMessage(content="What is 1234 multiplied by 5678?")]}

response = agent_executor.invoke(inputs)

# 5. Extract the result
# The last message in the state will be the AI's final answer
print(response["messages"][-1].content)
