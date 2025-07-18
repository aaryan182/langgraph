# Import necessary modules and classes
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv  # used to store secret stuff like API key

# Load environment variables from a .env file
load_dotenv()

# Define a typed dictionary to represent the agent's state
class AgentState(TypedDict):
    messages: List[HumanMessage]  # List of human messages

# Create an instance of the ChatOpenAI class, which will be used to interact with the OpenAI API
llm = ChatOpenAI(model='gpt-4o')  # Use the gpt-4o model for this example

# Define a function that processes the agent's state and generates a response
def process(state: AgentState) -> AgentState:
    # Use the llm instance to invoke the OpenAI API and get a response to the user's message
    response = llm.invoke(state['messages'])
    # Print the AI's response
    print(f"\nAI: {response.content}")
    # Return the updated state
    return state

# Create a state graph
graph = StateGraph(AgentState)

# Add a node to the graph that represents the processing function
graph.add_node("process", process)

# Add edges to the graph to define the flow of execution
graph.add_edge(START, "process")  # Start the graph at the "process" node
graph.add_edge("process", END)  # End the graph after the "process" node

# Compile the graph into an executable agent
agent = graph.compile()

# Get user input and interact with the agent
user_input = input("Enter: ")
while user_input != "exit":
    # Create a new state with the user's input as a HumanMessage
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    # Get the next user input
    user_input = input("Enter: ")