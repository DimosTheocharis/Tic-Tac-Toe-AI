from backend.components.state import State
from game import Game

# game: State = State(3, 3)

playerA: str = "X"
playerB: str = "O"
currentPlayer: str = playerA

stop: bool = False

# game.printGrid()
# print(f"Player {currentPlayer} is playing. Where do you wanna play?")
# row: int = int(input("Select row: "))
# column: int = int(input("Select column: "))
# stop = not game.play(currentPlayer, row, column)
# game.printGrid()

# currentPlayer = playerB if currentPlayer == playerA else playerA

# while (not stop):
#     print(f"Player {currentPlayer} is playing. Where do you wanna play?")
#     row: int = int(input("Select row: "))
#     column: int = int(input("Select column: "))

#     stop = not game.play(currentPlayer, row, column)
#     game.printGrid()

#     keepPlaying: str = input("You wanna keep playing (Y/N)?")
#     stop = True if keepPlaying == 'N' else False

#     currentPlayer = playerB if currentPlayer == playerA else playerA


game: Game = Game()
game.game.assignGrid([
    ['O','X','X'],
    ['X','O','X'],
    ['O','O','O']
]) 

game.game.printGrid()


game.isVictory()




