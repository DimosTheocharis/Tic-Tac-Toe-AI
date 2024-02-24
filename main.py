from backend.components.state import State
from backend.algorithms.miniMax import MiniMax
from game import Game
import time


game: Game = Game()

game.newGame()


a: State = State(3)
a.assignGrid([
    ['X', ' ', ' '],
    ['X', 'O', ' '],
    [' ', ' ', ' ']
])


miniMax: MiniMax = MiniMax('X', 'O')
miniMax.miniMax(a, 8, 'O').printGrid()









