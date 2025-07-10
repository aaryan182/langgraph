from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: str
    skills: list[str]
    final: str
    
def first_node(state:AgentState) -> AgentState:
    """This is the first node which personalises the name field with a greeting"""
    state['final'] = f'{state['name']} , welcome to the system!'
    return state

def second_node(state:AgentState) -> AgentState:
    """This is the second node which describes the users age"""
    state['final'] = state['final'] + f"You are {state['age']} years old!"
    return state

def third_node(state:AgentState) -> AgentState:
    """This is the third node which lists the users skills in a string"""
    skills_str = ', '.join(state['skills'])
    state['final'] += f"You have skills in: {skills_str}"
    return state

graph = StateGraph(AgentState)

graph.add_node('first_node', first_node)
graph.add_node('second_node', second_node)
graph.add_node('third_node', third_node)

graph.set_entry_point('first_node')
graph.add_edge('first_node', 'second_node')
graph.add_edge('second_node', 'third_node')
graph.set_finish_point('third_node')


app = graph.compile()

result = app.invoke({"name":"Aaryan", "age":"22", "skills":["python", "Machine", "Langgraph"]})

print(result)