# Import the TypedDict type from the typing module, which is used to define a dictionary with a specific structure
from typing import TypedDict

# Import the StateGraph class from the langgraph.graph module, which is used to define a graph of states
from langgraph.graph import StateGraph

# Define a class called AgentState, which is a TypedDict with four fields: 'name', 'age', 'skills', and 'final'
class AgentState(TypedDict):
    # The 'name' field is a string that will be used to store a name in the state
    name: str
    # The 'age' field is a string that will be used to store an age in the state
    age: str
    # The 'skills' field is a list of strings that will be used to store a list of skills in the state
    skills: list[str]
    # The 'final' field is a string that will be used to store the final message in the state
    final: str

# Define a function called first_node, which takes an AgentState as input and returns a new AgentState
def first_node(state: AgentState) -> AgentState:
    # This is the first node of our sequence, which personalizes the name field with a greeting
    """This is the first node which personalises the name field with a greeting"""
    # Set the final message to a greeting that includes the name
    state['final'] = f'{state['name']} , welcome to the system!'
    # Return the modified state
    return state

# Define a function called second_node, which takes an AgentState as input and returns a new AgentState
def second_node(state: AgentState) -> AgentState:
    # This is the second node of our sequence, which describes the user's age
    """This is the second node which describes the users age"""
    # Append the age to the final message
    state['final'] = state['final'] + f"You are {state['age']} years old!"
    # Return the modified state
    return state

# Define a function called third_node, which takes an AgentState as input and returns a new AgentState
def third_node(state: AgentState) -> AgentState:
    # This is the third node of our sequence, which lists the user's skills in a string
    """This is the third node which lists the users skills in a string"""
    # Join the list of skills into a string with commas
    skills_str = ', '.join(state['skills'])
    # Append the skills string to the final message
    state['final'] += f"You have skills in: {skills_str}"
    # Return the modified state
    return state

# Create a new StateGraph instance, passing in the AgentState class as the state type
graph = StateGraph(AgentState)

# Add a new node to the graph, called 'first_node', which is implemented by the first_node function
graph.add_node('first_node', first_node)

# Add a new node to the graph, called 'second_node', which is implemented by the second_node function
graph.add_node('second_node', second_node)

# Add a new node to the graph, called 'third_node', which is implemented by the third_node function
graph.add_node('third_node', third_node)

# Set the entry point of the graph to the 'first_node' node, which means that this node will be executed first
graph.set_entry_point('first_node')

# Add an edge from the 'first_node' node to the 'second_node' node, which means that the 'second_node' node will be executed after the 'first_node' node
graph.add_edge('first_node', 'second_node')

# Add an edge from the 'second_node' node to the 'third_node' node, which means that the 'third_node' node will be executed after the 'second_node' node
graph.add_edge('second_node', 'third_node')

# Set the finish point of the graph to the 'third_node' node, which means that this node will be executed last
graph.set_finish_point('third_node')

# Compile the graph into an executable application
app = graph.compile()

# Invoke the application with an input state that includes a name, age, and skills
result = app.invoke({"name": "Aaryan", "age": "22", "skills": ["python", "Machine", "Langgraph"]})

# Print the resulting state, which includes the final message
print(result)