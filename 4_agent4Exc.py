from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    number1: int
    operation: str
    number2: int
    number3: int
    number4: int
    operation2: str
    finalNumber: int
    finalNumber2: int

# First operation nodes
def adder(state: AgentState) -> AgentState:
    state['finalNumber'] = state['number1'] + state['number2']
    return state

def subtractor(state: AgentState) -> AgentState:
    state['finalNumber'] = state['number1'] - state['number2']
    return state

def decide_next_node(state: AgentState) -> str:
    if state['operation'] == "+":
        return "add_node"
    elif state['operation'] == "-":
        return "subtract_node"
    else:
        raise ValueError(f"Unsupported operation: {state['operation']}")

# Second operation nodes
def adder2(state: AgentState) -> AgentState:
    state['finalNumber2'] = state['number3'] + state['number4']
    return state

def subtractor2(state: AgentState) -> AgentState:
    state['finalNumber2'] = state['number3'] - state['number4']
    return state

def decide_next_node2(state: AgentState) -> str:
    if state['operation2'] == "+":
        return "add_node2"
    elif state['operation2'] == "-":
        return "subtract_node2"
    else:
        raise ValueError(f"Unsupported operation2: {state['operation2']}")

# Build graph
graph = StateGraph(AgentState)

graph.add_node("add_node", adder)
graph.add_node("subtract_node", subtractor)
graph.add_node("router", lambda state: state)

graph.add_node("add_node2", adder2)
graph.add_node("subtract_node2", subtractor2)
graph.add_node("router2", lambda state: state)

# Start → first router
graph.add_edge(START, "router")

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

# Compile
app = graph.compile()

# Test input
initial_state = {
    "number1": 10, "operation": "-", "number2": 5,
    "number3": 7, "number4": 2, "operation2": "+",
    "finalNumber": 0, "finalNumber2": 0
}

result = app.invoke(initial_state)
print(result)
