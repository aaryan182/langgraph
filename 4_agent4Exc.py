# Import the TypedDict type from the typing module, which is used to define a dictionary with a specific structure
from typing import TypedDict

# Import the StateGraph class and START and END constants from the langgraph.graph module
from langgraph.graph import StateGraph, START, END

# Define a class called AgentState, which is a TypedDict with eight fields: 'number1', 'operation', 'number2', 'number3', 'number4', 'operation2', 'finalNumber', and 'finalNumber2'
class AgentState(TypedDict):
    # The 'number1' field is an integer that will be used to store the first number in the state
    number1: int
    # The 'operation' field is a string that will be used to store the operation to be performed in the state
    operation: str
    # The 'number2' field is an integer that will be used to store the second number in the state
    number2: int
    # The 'number3' field is an integer that will be used to store the third number in the state
    number3: int
    # The 'number4' field is an integer that will be used to store the fourth number in the state
    number4: int
    # The 'operation2' field is a string that will be used to store the second operation to be performed in the state
    operation2: str
    # The 'finalNumber' field is an integer that will be used to store the result of the first operation in the state
    finalNumber: int
    # The 'finalNumber2' field is an integer that will be used to store the result of the second operation in the state
    finalNumber2: int

# First operation nodes
def adder(state: AgentState) -> AgentState:
    # This node adds the two numbers in the state
    state['finalNumber'] = state['number1'] + state['number2']
    return state

def subtractor(state: AgentState) -> AgentState:
    # This node subtracts the two numbers in the state
    state['finalNumber'] = state['number1'] - state['number2']
    return state

def decide_next_node(state: AgentState) -> str:
    # This function decides which operation to perform based on the operation field in the state
    if state['operation'] == "+":
        return "add_node"
    elif state['operation'] == "-":
        return "subtract_node"
    else:
        raise ValueError(f"Unsupported operation: {state['operation']}")

# Second operation nodes
def adder2(state: AgentState) -> AgentState:
    # This node adds the two numbers in the state
    state['finalNumber2'] = state['number3'] + state['number4']
    return state

def subtractor2(state: AgentState) -> AgentState:
    # This node subtracts the two numbers in the state
    state['finalNumber2'] = state['number3'] - state['number4']
    return state

def decide_next_node2(state: AgentState) -> str:
    # This function decides which operation to perform based on the operation2 field in the state
    if state['operation2'] == "+":
        return "add_node2"
    elif state['operation2'] == "-":
        return "subtract_node2"
    else:
        raise ValueError(f"Unsupported operation2: {state['operation2']}")

# Build graph
graph = StateGraph(AgentState)

# Add nodes for the first operation
graph.add_node("add_node", adder)
graph.add_node("subtract_node", subtractor)
graph.add_node("router", lambda state: state)

# Add nodes for the second operation
graph.add_node("add_node2", adder2)
graph.add_node("subtract_node2", subtractor2)
graph.add_node("router2", lambda state: state)

# Start → first router
graph.add_edge(START, "router")

# Add conditional edges from the first router to the first operation nodes
graph.add_conditional_edges(
    "router",
    decide_next_node,
    {
        "add_node": "add_node",
        "subtract_node": "subtract_node"
    }
)

# After first operation → second router
graph.add_edge("add_node", "router2")
graph.add_edge("subtract_node", "router2")

# Add conditional edges from the second router to the second operation nodes
graph.add_conditional_edges(
    "router2",
    decide_next_node2,
    {
        "add_node2": "add_node2",
        "subtract_node2": "subtract_node2"
    }
)

# Final nodes → END
graph.add_edge("add_node2", END)
graph.add_edge("subtract_node2", END)

#