# Import the TypedDict type from the typing module, which is used to define a dictionary with a specific structure
from typing import TypedDict

# Import the StateGraph class and START and END constants from the langgraph.graph module
from langgraph.graph import StateGraph, START, END

# Define a class called AgentState, which is a TypedDict with four fields: 'number1', 'operation', 'number2', and 'finalNumber'
class AgentState(TypedDict):
    # The 'number1' field is an integer that will be used to store the first number in the state
    number1: int
    # The 'operation' field is a string that will be used to store the operation to be performed in the state
    operation: str
    # The 'number2' field is an integer that will be used to store the second number in the state
    number2: int
    # The 'finalNumber' field is an integer that will be used to store the result of the operation in the state
    finalNumber: int

# Define a function called adder, which takes an AgentState as input and returns a new AgentState
def adder(state: AgentState) -> AgentState:
    # This node adds the two numbers in the state
    """This node adds the 2 numbers"""
    # Set the finalNumber field to the sum of the two numbers
    state['finalNumber'] = state['number1'] + state['number2']
    # Return the modified state
    return state

# Define a function called subtractor, which takes an AgentState as input and returns a new AgentState
def subtractor(state: AgentState) -> AgentState:
    # This node subtracts the two numbers in the state
    """This node subtracts the 2 numbers"""
    # Set the finalNumber field to the difference of the two numbers
    state['finalNumber'] = state['number1'] - state['number2']
    # Return the modified state
    return state

# Define a function called decide_next_node, which takes an AgentState as input and returns a string
def decide_next_node(state: AgentState) -> str:
    # This function decides which operation to perform based on the operation field in the state
    """Decides which operation to perform"""
    # If the operation is "+", return "add_node"
    if state['operation'] == "+":
        return "add_node"
    # If the operation is "-", return "subtract_node"
    elif state['operation'] == "-":
        return "subtract_node"
    # If the operation is not supported, raise a ValueError
    else:
        raise ValueError(f"Unsupported operation: {state['operation']}")

# Create a new StateGraph instance, passing in the AgentState class as the state type
graph = StateGraph(AgentState)

# Add a new node to the graph, called "add_node", which is implemented by the adder function
graph.add_node("add_node", adder)

# Add a new node to the graph, called "subtract_node", which is implemented by the subtractor function
graph.add_node("subtract_node", subtractor)

# Add a new node to the graph, called "router", which is a lambda function that just passes through the state
graph.add_node("router", lambda state: state)

# Add an edge from the START node to the "router" node
graph.add_edge(START, "router")

# Add conditional edges from the "router" node to the "add_node" and "subtract_node" nodes
# The decide_next_node function is used to determine which edge to take based on the operation field in the state
graph.add_conditional_edges(
    "router",
    decide_next_node,
    {
        "add_node": "add_node",
        "subtract_node": "subtract_node"
    }
)

# Add edges from the "add_node" and "subtract_node" nodes to the END node
graph.add_edge("add_node", END)
graph.add_edge("subtract_node", END)

# Compile the graph into an executable application
app = graph.compile()

# Define an initial state with numbers 10 and 5, operation "-", and finalNumber 0
initial_state_1 = {
    "number1": 10,
    "operation": "-",
    "number2": 5,
    "finalNumber": 0
}

# Invoke the application with the initial state
result = app.invoke(initial_state_1)

# Print the resulting state
print(result)