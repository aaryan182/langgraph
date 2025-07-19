# Import necessary modules and classes
from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_core.messages import ToolMessage
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Load environment variables from a .env file
load_dotenv()

# Define a type annotation for an email address
email = Annotated[str, "This has to be a valid email format"]

# Define a reducer function that combines updates from nodes with the existing state
# This function is used to merge new data into the current state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Define a tool that adds two numbers together
@Tool
def add(a: int, b: int):
    """This is an addition function that adds 2 numbers together"""
    return a + b

# Define a tool that subtracts two numbers together
@Tool
def subtract(a: int, b: int):
    """This is a subtraction function that subtracts 2 numbers together"""
    return a - b

# Define a tool that multiplies two numbers together
@Tool
def multiply(a: int, b: int):
    """This is a multiplication function that multiplies 2 numbers together"""
    return a * b

# Define a list of tools
tools = [add, subtract, multiply]

# Create a ChatOpenAI model and bind the tools to it
model = ChatOpenAI(model='gpt-4o').bind_tools(tools)

# Define a function that calls the model with the current state
def model_call(state: AgentState) -> AgentState:
    # Create a system prompt that tells the model to answer the user's query
    system_prompt = SystemMessage(content="You are my AI assistant, please answer my query to the best of your ability")
    # Invoke the model with the system prompt and the current state
    response = model.invoke([system_prompt] + list(state["messages"]))
    # Return the updated state with the model's response
    return {"messages": [response]}

# Define a function that determines whether to continue or end the conversation
def should_continue(state: AgentState):
    # Get the last message in the conversation
    messages = state['messages']
    last_message = messages[-1]
    # If the last message has no tool calls, end the conversation
    if not last_message.tool_calls:
        return 'end'
    # Otherwise, continue the conversation
    else:
        return 'continue'

# Create a state graph
graph = StateGraph(AgentState)

# Add a node to the graph that calls the model
graph.add_node("our_agent", model_call)

# Create a tool node that represents the tools
tool_node = ToolNode(tools=tools)
graph.add_node('tools', tool_node)

# Set the entry point of the graph to the model node
graph.set_entry_point('our_agent')

# Add conditional edges to the graph that determine whether to continue or end the conversation
graph.add_conditional_edges(
    'our_agent',
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)

# Add an edge from the tool node back to the model node
graph.add_edge("tools", "our_agent")

# Compile the graph into an executable app
app = graph.compile()

# Define a function that prints the conversation stream
def print_stream(stream):
    # Iterate over the conversation stream
    for s in stream:
        # Get the last message in the stream
        message = s['messages'][-1]
        # If the message is a tuple, print it
        if isinstance(message, tuple):
            print(message)
        # Otherwise, pretty-print the message
        else:
            message.pretty_print()

# Define an input to the app
inputs = {"messages": [("user", "Add 40 + 30 and then subtract the result by 20 and then multiply the result by 50")]}

# Print the conversation stream
print_stream(app.stream(inputs, stream_mode='values'))