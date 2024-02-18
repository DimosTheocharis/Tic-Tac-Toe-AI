from backend.components.state import State
from backend.algorithms.miniMax import MiniMax
from game import Game
import time

miniMax: MiniMax = MiniMax('X', 'O')



# b: State = State(3)
# b.assignGrid([
#     ['X', 'O', ' '],
#     [' ', ' ', 'O'],
#     ['X', 'O', 'X']
# ])



# print(miniMax.evaluationFunction(b, 'X'))


a = State(3)
a.assignGrid([
    ['X', 'O', ' '],
    ['O', 'O', 'X'],
    [' ', ' ', 'X']
])

start = time.time()
nextMove: State = miniMax.miniMax(a, 2, 'X')
nextMove.printGrid()
end = time.time()
print(f"time: {end - start}")




