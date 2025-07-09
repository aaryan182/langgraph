from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str
    operation: str
    
def calc(values: List[int], operation: str)-> int:
    if operation == "+":
        return sum(values)
    elif operation == "*":
        result = 1
        for v in values:
            result *= v
        return result
    else:
        raise ValueError(f"Unsupported operation: {operation}")

def process_values(state: AgentState) -> AgentState:
    """"Process values based on operation (+ or *)"""
    
    answer = calc(state["values"], state["operation"])
    state["result"] = f"Hi {state['name']}, your answer is: {answer}"
    return state

graph = StateGraph(AgentState)

graph.add_node("processor", process_values)

graph.set_entry_point("processor")
graph.set_finish_point("processor")

graph = graph.compile()

input_state = {
    "name": "Aaryan Bajaj",
    "values": [1,2,3,4],
    "operation": "*",
    "result": ""
}

output_state = graph.invoke(input_state)

print(output_state["result"])