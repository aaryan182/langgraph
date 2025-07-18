# Learn how to handle multiple inputs

# Import the TypedDict and List types from the typing module, which are used to define a dictionary with a specific structure and a list of values
from typing import TypedDict, List

# Import the StateGraph class from the langgraph.graph module, which is used to define a graph of states
from langgraph.graph import StateGraph

# Define a class called AgentState, which is a TypedDict with three fields: 'values', 'name', and 'result'
class AgentState(TypedDict):
    # The 'values' field is a list of integers that will be used to store a list of values in the state
    values: List[int]
    # The 'name' field is a string that will be used to store a name in the state
    name: str
    # The 'result' field is a string that will be used to store the result of processing the values and name
    result: str

# Define a function called process_values, which takes an AgentState as input and returns a new AgentState
def process_values(state: AgentState) -> AgentState:
    # This function handles multiple different inputs by processing the values and name in the state
    """This function handles multiple different inputs"""
    
    # Calculate the sum of the values in the state and create a result message that includes the name and sum
    state["result"] = f"Hi there {state["name"]}! Your sum = {sum(state["values"])}"
    
    # Return the modified state with the result message
    return state

# Create a new StateGraph instance, passing in the AgentState class as the state type
graph = StateGraph(AgentState)

# Add a new node to the graph, called "processor", which is implemented by the process_values function
graph.add_node("processor", process_values)

# Set the entry point of the graph to the "processor" node, which means that this node will be executed first
graph.set_entry_point("processor")

# Set the finish point of the graph to the "processor" node, which means that this node will be executed last
# Since there is only one node in the graph, the entry and finish points are the same
graph.set_finish_point("processor")

# Compile the graph into an executable application
app = graph.compile()

# Invoke the application, passing in an initial state with values [1, 2, 3, 4] and name "Aaryan"
answers = app.invoke({"values": [1, 2, 3, 4], "name": "Aaryan"})

# Print the resulting state, which includes the result message
print(answers)

# Print the result message from the resulting state
print(answers["result"])