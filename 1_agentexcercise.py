from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    message: str
    
def congrats_node(state: AgentState) -> AgentState:
    """Simple node that adds a congratulations message to the state"""
    
    state['message'] = state["message"] + ", you are doing an amazing job learning langgraph"
    
    return state

graph = StateGraph(AgentState)

graph.add_node("congratulations", congrats_node)

graph.set_entry_point("congratulations")
graph.set_finish_point("congratulations")

app = graph.compile()

result = app.invoke({"message": "aaryan"})

result["message"]