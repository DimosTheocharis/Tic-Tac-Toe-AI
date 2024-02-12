from backend.components.state import State

class Game:
    def __init__(self):
        self.dimension: int = 3
        self.playerA: str = "X"
        self.playerB: str = "O"  
        self.currentPlayer: str = self.playerA

    def newGame(self):
        '''
            Starts a new game.
        '''
        self.state = State(self.dimension)
        while (not (self.state.isVictory() or self.state.gridIsFull())):
            self.state.printGrid()
            coordinates: tuple[int, int] = self.receivePlayerInput()

            while(not self.state.play(self.currentPlayer, coordinates[0], coordinates[1])):
                print("Please try again")
                self.state.printGrid()
                coordinates = self.receivePlayerInput()
                
            self.switchTurn()
            print("")

        self.state.printGrid()
        if (self.state.isVictory()):
            self.switchTurn()
            print(f"Player {self.currentPlayer} wins!")
        else:
            print("The game results to tie!")


    def switchTurn(self) -> None:
        '''
            Handles the switching of the player playing.
        '''
        self.currentPlayer = self.playerB if self.currentPlayer == self.playerA else self.playerA


    def receivePlayerInput(self) -> tuple[int, int]:
        '''
            Asks current player to give the coordinates (row, column) of the cell where we wants to place his symbol

            Returns:
                tuple[int, int]: the (row, column) coordinates of the cell
        '''
        print(f"Player {self.currentPlayer} is playing. Where do you wanna play?")

        row: int = int(input("Select row: "))
        column: int = int(input("Select column: "))

        return (row, column)

    
        