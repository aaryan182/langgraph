# Import the StateGraph class and END constant from the langgraph.graph module
from langgraph.graph import StateGraph, END

# Import the random module for generating random numbers
import random

# Import the TypedDict type from the typing module, which is used to define a dictionary with a specific structure
from typing import Dict, List, TypedDict

# Define a class called AgentState, which is a TypedDict with three fields: 'name', 'number', and 'counter'
class AgentState(TypedDict):
    # The 'name' field is a string that will be used to store a name in the state
    name: str
    # The 'number' field is a list of integers that will be used to store a list of numbers in the state
    number: List[int]
    # The 'counter' field is an integer that will be used to store a counter in the state
    counter: int

# Define a function called greeting_node, which takes an AgentState as input and returns a new AgentState
def greeting_node(state: AgentState) -> AgentState:
    # This node generates a greeting message for the person in the state
    """Greeting Node which says hi to the person"""
    # Set the name field to a greeting message that includes the person's name
    state['name'] = f"Hi there, {state['name']}"
    # Set the counter field to 0
    state['counter'] = 0
    # Return the modified state
    return state

# Define a function called random_node, which takes an AgentState as input and returns a new AgentState
def random_node(state: AgentState) -> AgentState:
    # This node generates a random number between 0 and 10 and adds it to the list of numbers in the state
    """Generates a random number from 0 to 10 """
    # Generate a random number between 0 and 10
    random_number = random.randint(0, 10)
    # Add the random number to the list of numbers in the state
    state['number'].append(random_number)
    # Increment the counter field by 1
    state['counter'] += 1
    # Return the modified state
    return state

# Define a function called should_continue, which takes an AgentState as input and returns a string
def should_continue(state: AgentState) -> str:
    # This function decides what to do next based on the counter field in the state
    """Function to decide what to do next"""
    # If the counter field is less than 5, return "loop" to continue the loop
    if state['counter'] < 5:
        print("Entering LOOP", state['counter'])
        return "loop"
    # If the counter field is 5 or more, return "exit" to exit the loop
    else:
        return "exit"

# Create a new StateGraph instance
graph = StateGraph(AgentState)

# Add a node to the graph called "greeting" that is implemented by the greeting_node function
graph.add_node("greeting", greeting_node)

# Add a node to the graph called "random" that is implemented by the random_node function
graph.add_node("random", random_node)

# Add an edge from the "greeting" node to the "random" node
graph.add_edge("greeting", "random")

# Add conditional edges from the "random" node to itself and to the END node
graph.add_conditional_edges(
    "random",  # source node
    should_continue,  # action
    {
        "loop": "random",  # self-loop back to the same node
        "exit": END  # end the graph
    }
)

# Set the entry point of the graph to the "greeting" node
graph.set_entry_point("greeting")

# Compile the graph into an executable application
app = graph.compile()

# Invoke the application with an initial state that includes a name, an empty list of numbers, and a counter of -1
app.invoke({"name": "Aaryan", "number": [], "counter": -1})