from backend.components.state import State
from backend.algorithms.miniMax import MiniMax
from game import Game
import time

miniMax: MiniMax = MiniMax('X', 'O')


a = State(3)
a.assignGrid([
    ['X', 'O', ' '],
    ['O', 'O', ' '],
    ['X', ' ', ' ']
])

start = time.time()
nextMove: State = miniMax.miniMax(a, 10, 'X')
nextMove.printGrid()
end = time.time()
print(f"time: {end - start}")




