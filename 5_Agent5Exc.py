# Import necessary modules and classes
from langgraph.graph import StateGraph, END
import random
from typing import Dict, List, TypedDict

# Define a typed dictionary to represent the agent's state
class AgentState(TypedDict):
    player_name: str
    guesses: List[int]
    attempts: int
    lower_bound: int
    upper_bound: int
    secret_number: int
    last_guess: int

# Define a node that makes a guess
def guess_node(state: AgentState) -> AgentState:
    # Calculate the next guess as the midpoint of the current bounds
    guess = (state["lower_bound"] + state["upper_bound"]) // 2
    # Update the state with the new guess
    state['last_guess'] = guess
    state['guesses'].append(guess)
    state['attempts'] += 1
    # Print the current attempt and guess
    print(f"[Attempt {state['attempts']}] Guess: {guess}")
    return state

# Define a node that provides a hint based on the previous guess
def hint_node(state: AgentState) -> str:
    # Check if the previous guess was correct
    if state['last_guess'] == state['secret_number']:
        print("Correct guess")
        return 'correct'
    # Check if the maximum number of attempts has been reached
    elif state['attempts'] >= 7:
        print('Max attempts reached')
        return 'fail'
    # If the previous guess was too low, update the lower bound
    elif state['last_guess'] < state['secret_number']:
        state['lower_bound'] = state['last_guess'] + 1
        print("higher")
        return 'continue'
    # If the previous guess was too high, update the upper bound
    else:
        state['upper_bound'] = state['last_guess'] - 1
        print('lower')
        return 'continue'

# Create a state graph
graph = StateGraph(AgentState)

# Add nodes to the graph
graph.add_node('guess', guess_node)
graph.add_node('hint', lambda s: s)  # This node does nothing, just passes the state through

# Set the entry point of the graph to the 'guess' node
graph.set_entry_point('guess')

# Add an edge from the 'guess' node to the 'hint' node
graph.add_edge('guess', 'hint')

# Add conditional edges from the 'hint' node based on the hint node's output
graph.add_conditional_edges(
    'hint',
    hint_node,
    {
        "continue": 'guess',  # If the hint is 'continue', go back to the 'guess' node
        'correct': END,  # If the hint is 'correct', end the graph
        'fail': END  # If the hint is 'fail', end the graph
    }
)

# Compile the graph into an executable app
app = graph.compile()

# Define an initial state for the app
initial_state = {
    'player_name': "Aaryan",
    'guesses': [],
    'attempts': 0,
    'lower_bound': 1,
    'upper_bound': 20,
    'secret_number': random.randint(1, 20),
    'last_guess': 0
}

# Print the secret number for debugging purposes
print(f'Secret number is: {initial_state["secret_number"]}')

# Run the app with the initial state and print the final state
result = app.invoke(initial_state)
print('Final State', result)