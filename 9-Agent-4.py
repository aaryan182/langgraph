# Import necessary libraries
from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Load environment variables from .env file
load_dotenv()

# Global variable to store document content
document_content = ""

# Define a TypedDict for AgentState
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Define a tool to update the document content
@tool
def update(content: str) -> str:
    """Updates the documents with the provided content"""
    global document_content
    document_content = content
    return f"Document has been updated successfully! The current content is: \n {document_content}"

# Define a tool to save the document to a text file
@tool
def save(filename: str) -> str:
    """Save the current document to a text file and finish the process.
    
    Args: 
        filename: Name for the text file
    """
    global document_content
    
    if not filename.endswith('.txt'):
        filename = f"{filename}.txt"
        
    try:
        with open(filename, 'w') as file:
            file.write(document_content)
        print(f"\n Document has been saved to: {filename}")
        return f"Document has been saved successfully to '{filename}'."
    
    except Exception as e:
        return f"Error saving document: {str(e)}"

# Define a list of tools
tools = [update, save]

# Create a ChatOpenAI model and bind it to the tools
model = ChatOpenAI(model='gpt-4o').bind_tools(tools)

# Define the agent function
def our_agent(state: AgentState) -> AgentState:
    # Define a system prompt to introduce the agent
    system_prompt = SystemMessage(content = f"""
    You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.
        
    - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
    - If the user wants to save and finish, you need to use the 'save' tool.
    - Make sure to always show the current document state after modifications.
        
    The current document content is:{document_content}
    """)
    
    # Check if this is the first message
    if not state["messages"]:
        user_input = "I'm ready to help you update a document. What would you like to create?"
        user_message = HumanMessage(content=user_input)
    
    # Otherwise, get the user input
    else:
        user_input = input("\nWhat would you like to do with the document? ")
        print(f"\n USER: {user_input}")
        user_message = HumanMessage(content=user_input)

    # Create a list of all messages
    all_messages = [system_prompt] + list(state["messages"]) + [user_message]

    # Invoke the model with the messages
    response = model.invoke(all_messages)

    # Print the response
    print(f"\n AI: {response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f" USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")

    # Return the updated state
    return {"messages": list(state["messages"]) + [user_message, response]}

# Define a function to determine if the conversation should continue
def should_continue(state: AgentState) -> str:
    """Determine if we should continue or end the conversation."""
    
    # Get the list of messages
    messages = state["messages"]
    
    # Check if there are no messages
    if not messages:
        return "continue"
    
    # Check if the last message is a ToolMessage resulting from save
    for message in reversed(messages):
        if (isinstance(message, ToolMessage) and 
            "saved" in message.content.lower() and
            "document" in message.content.lower()):
            return "end" # goes to the end edge which leads to the endpoint
        
    # Otherwise, continue the conversation
    return "continue"

# Define a function to print the messages in a more readable format
def print_messages(messages):
    """Function I made to print the messages in a more readable format"""
    if not messages:
        return
    
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"\n TOOL RESULT: {message.content}")

# Create a StateGraph
graph = StateGraph(AgentState)

# Add nodes to the graph

graph.add_node("agent", our_agent)
graph.add_node("tools", ToolNode(tools))

graph.set_entry_point("agent")

graph.add_edge("agent", "tools")


graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue": "agent",
        "end": END,
    },
)

app = graph.compile()

def run_document_agent():
    print("\n ===== DRAFTER =====")
    
    state = {"messages": []}
    
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
    
    print("\n ===== DRAFTER FINISHED =====")

if __name__ == "__main__":
    run_document_agent()