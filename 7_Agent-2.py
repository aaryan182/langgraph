# Import necessary modules and classes
import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Define a typed dictionary to represent the agent's state
class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]  # List of human and AI messages

# Create an instance of the ChatOpenAI class, which will be used to interact with the OpenAI API
llm = ChatOpenAI(model='gpt-4o')  # Use the gpt-4o model for this example

# Define a function that processes the agent's state and generates a response
def process(state: AgentState) -> AgentState:
    """This node will solve the request you input"""
    # Use the llm instance to invoke the OpenAI API and get a response to the user's message
    response = llm.invoke(state['messages'])
    
    # Append the AI's response to the state's message list
    state['messages'].append(AIMessage(content=response.content))
    # Print the AI's response
    print(f"\nAI: {response.content}")
    # Print the current state (i.e., the conversation history)
    print("Current State: ", state["messages"])
    
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

# Initialize an empty conversation history
conversation_history = []

# Get user input and interact with the agent
user_input = input("Enter: ")
while user_input != "exit":
    # Create a new human message from the user's input
    conversation_history.append(HumanMessage(content=user_input))
    # Invoke the agent with the current conversation history
    result = agent.invoke({"messages": conversation_history})
    # Update the conversation history with the agent's response
    conversation_history = result['messages']
    # Get the next user input
    user_input = input("Enter: ")

# Save the conversation history to a file
with open("logging.txt", "w") as file:
    file.write("Your conversation Log: \n")
    # Iterate over the conversation history and write each message to the file
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n\n")
    file.write("end of conversation")

# Print a success message
print("conversation saved to logging.txt")