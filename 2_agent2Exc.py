# Import the TypedDict and List types from the typing module, which are used to define a dictionary with a specific structure and a list of values
from typing import TypedDict, List

# Import the StateGraph class from the langgraph.graph module, which is used to define a graph of states
from langgraph.graph import StateGraph

# Define a class called AgentState, which is a TypedDict with four fields: 'values', 'name', 'result', and 'operation'
class AgentState(TypedDict):
    # The 'values' field is a list of integers that will be used to store a list of values in the state
    values: List[int]
    # The 'name' field is a string that will be used to store a name in the state
    name: str
    # The 'result' field is a string that will be used to store the result of processing the values and operation
    result: str
    # The 'operation' field is a string that will be used to store the operation to be performed on the values
    operation: str

# Define a function called calc, which takes a list of integers and an operation as input and returns an integer
def calc(values: List[int], operation: str) -> int:
    # This function performs the specified operation on the list of values
    if operation == "+":
        # If the operation is "+", return the sum of the values
        return sum(values)
    elif operation == "*":
        # If the operation is "*", return the product of the values
        result = 1
        for v in values:
            result *= v
        return result
    else:
        # If the operation is not supported, raise a ValueError
        raise ValueError(f"Unsupported operation: {operation}")

# Define a function called process_values, which takes an AgentState as input and returns a new AgentState
def process_values(state: AgentState) -> AgentState:
    # This function processes the values based on the operation specified in the state
    """"Process values based on operation (+ or *)"""
    
    # Call the calc function to perform the operation on the values
    answer = calc(state["values"], state["operation"])
    
    # Create a result message that includes the name and answer
    state["result"] = f"Hi {state['name']}, your answer is: {answer}"
    
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
graph = graph.compile()

# Define an input state with values [1, 2, 3, 4], name "Aaryan Bajaj", operation "*", and an empty result
input_state = {
    "name": "Aaryan Bajaj",
    "values": [1, 2, 3, 4],
    "operation": "*",
    "result": ""
}

# Invoke the application with the input state
output_state = graph.invoke(input_state)

# Print the result message from the output state
print(output_state["result"])