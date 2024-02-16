from backend.components.state import State
from backend.algorithms.miniMax import MiniMax
from game import Game


myState: State = State(3)
myState.assignGrid([
    [' ', ' ', ' '],
    [' ', ' ', 'O'],
    [' ', 'O', 'O']
])

miniMax: MiniMax = MiniMax('X', 'O')

evaluation = miniMax.evaluationFunction(myState, 'O')

print(evaluation)


a = State(3)
a.assignGrid([
    ['X', ' ', ' '],
    [' ', 'X', 'O'],
    ['X', 'O', 'O']
])

for x in a.getChildStates('Y'):
    print(x.grid)




