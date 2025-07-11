from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    number1: int
    operation: str
    number2: int
    finalNumber: int

def adder(state: AgentState) -> AgentState:
    """This node adds the 2 numbers"""
    state['finalNumber'] = state['number1'] + state['number2']
    return state

def subtractor(state: AgentState) -> AgentState:
    """This node subtracts the 2 numbers"""
    state['finalNumber'] = state['number1'] - state['number2']
    return state

def decide_next_node(state: AgentState) -> str:
    """Decides which operation to perform"""
    if state['operation'] == "+":
        return "add_node"
    elif state['operation'] == "-":
        return "subtract_node"
    else:
        raise ValueError(f"Unsupported operation: {state['operation']}")

graph = StateGraph(AgentState)

graph.add_node("add_node", adder)
graph.add_node("subtract_node", subtractor)
graph.add_node("router", lambda state: state)  # just passes through

graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router",
    decide_next_node,
    {
        "add_node": "add_node",
        "subtract_node": "subtract_node"
    }
)

graph.add_edge("add_node", END)
graph.add_edge("subtract_node", END)

app = graph.compile()

initial_state_1 = {
    "number1": 10,
    "operation": "-",
    "number2": 5,
    "finalNumber": 0  # optional, gets overwritten
}

result = app.invoke(initial_state_1)
print(result)
