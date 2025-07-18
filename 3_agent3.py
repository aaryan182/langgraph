# Import the TypedDict type from the typing module, which is used to define a dictionary with a specific structure
from typing import TypedDict

# Import the StateGraph class from the langgraph.graph module, which is used to define a graph of states
from langgraph.graph import StateGraph

# Define a class called AgentState, which is a TypedDict with three fields: 'name', 'age', and 'final'
class AgentState(TypedDict):
    # The 'name' field is a string that will be used to store a name in the state
    name: str
    # The 'age' field is a string that will be used to store an age in the state
    age: str
    # The 'final' field is a string that will be used to store the final message in the state
    final: str

# Define a function called first_node, which takes an AgentState as input and returns a new AgentState
def first_node(state: AgentState) -> AgentState:
    # This is the first node of our sequence, which sets the final message to a greeting
    """This is the first node of our sequence"""
    # Set the final message to a greeting that includes the name
    state['final'] = f"Hi {state["name"]}!"
    # Return the modified state
    return state

# Define a function called second_node, which takes an AgentState as input and returns a new AgentState
def second_node(state: AgentState) -> AgentState:
    # This is the second node of our sequence, which appends the age to the final message
    """This is the second node of our sequence"""
    # Append the age to the final message
    state['final'] = state['final'] + f"You are {state['age']} years old"
    # Return the modified state
    return state

# Create a new StateGraph instance, passing in the AgentState class as the state type
graph = StateGraph(AgentState)

# Add a new node to the graph, called 'first_node', which is implemented by the first_node function
graph.add_node('first_node', first_node)

# Add a new node to the graph, called 'second_node', which is implemented by the second_node function
graph.add_node('second_node', second_node)

# Set the entry point of the graph to the 'first_node' node, which means that this node will be executed first
graph.set_entry_point('first_node')

# Add an edge from the 'first_node' node to the 'second_node' node, which means that the 'second_node' node will be executed after the 'first_node' node
graph.add_edge('first_node', 'second_node')

# Set the entry point of the graph to the 'second_node' node, which means that this node will be executed last
# Note: This is not necessary, as the graph will automatically execute the nodes in the order they are added
graph.set_entry_point('second_node')

# Compile the graph into an executable application
app = graph.compile()

# Invoke the application with an input state that includes a name and age
result = app.invoke({"name": "Aaryan", "age": 22})

# Print the resulting state, which includes the final message
print(result)