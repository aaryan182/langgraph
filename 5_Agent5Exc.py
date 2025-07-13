from langgraph.graph import StateGraph, END
import random
from typing import Dict, List, TypedDict

class AgentState(TypedDict):
    player_name: str
    guesses: List[int]
    attempts: int
    lower_bound: int
    upper_bound: int
    secret_number: int
    last_guess: int

# Guessing node
def guess_node(state: AgentState) -> AgentState:
    guess = (state["lower_bound"] + state["upper_bound"])// 2
    state['last_guess'] = guess
    state['guesses'].append(guess)
    state['attempts'] += 1
    print(f"[Attempt {state['attempts']}] Guess: {guess}")
    return state

# Hint node
def hint_node(state: AgentState) -> str:
    if state['last_guess'] == state['secret_number']:
        print("Correct guess")
        return 'correct'
    elif state['attempts'] >= 7:
        print('Max attempts reached')
        return 'fail'
    elif state['last_guess'] < state['secret_number']:
        state['lower_bound'] = state['last_guess'] + 1
        print("higher")
        return 'continue'
    else:
        state['upper_bound'] = state['last_guess'] - 1
        print('lower')
        return 'continue'

graph = StateGraph(AgentState)

graph.add_node('guess', guess_node)
graph.add_node('hint', lambda s: s) 

graph.set_entry_point('guess')
graph.add_edge('guess', 'hint')

graph.add_conditional_edges(
    'hint',
    hint_node,
    {
        "continue": 'guess',
        'correct': END,
        'fail': END
    }
)

app = graph.compile()

initial_state = {
    'player_name': "Aaryan",
    'guesses': [],
    'attempts': 0,
    'lower_bound': 1,
    'upper_bound': 20,
    'secret_number': random.randint(1,20),
    'last_guess': 0
}

print(f'Secret number is: {initial_state['secret_number']}')

result = app.invoke(initial_state)
print('Final State', result)