from typing import Dict, List, Tuple
from backend.components.state import State
from backend.algorithms.miniMax import MiniMax

class Game:
    def __init__(self):
        self.dimension: int = 3
        self.playerA: str = "X"
        self.playerB: str = "O"  
        self.currentPlayer: str = self.playerA
        self.__computerIsPlaying: bool = False
        self.__miniMax: MiniMax = MiniMax(self.playerA, self.playerB)

    def newGame(self):
        '''
            Starts a new game.
        '''
        self.state = State(self.dimension)
        while (not (self.state.isVictory() or self.state.gridIsFull())):
            self.state.printGrid()
            print("")
            if (self.__computerIsPlaying):
                nextState: State = self.__miniMax.miniMax(self.state, 8, self.currentPlayer)

                stateDifference: Dict[str, List[Tuple[int, int, str]]] = self.findDifferencesBetweenStates(self.state, nextState)

                if (len(stateDifference["plus"]) == 1 and len(stateDifference["minus"]) == 0 and len(stateDifference["diff"]) == 0):
                    coordinates: tuple[int, int] = (stateDifference["plus"][0][0], stateDifference["plus"][0][1])
                    self.state.play(self.currentPlayer, coordinates[0], coordinates[1])
                    print(f"Computer placed {self.currentPlayer} in (row, column) = ({coordinates[0]},{coordinates[1]})")

            else:
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
        self.__computerIsPlaying = not self.__computerIsPlaying


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
    

    def findDifferencesBetweenStates(self, stateA: State, stateB: State) -> Dict[str, List[Tuple[int, int, str]]]:
        '''
            Finds the differences between 2 states. There can be 3 types of differences:
            a) plus: A symbol exists in stateB at certain cell, but the same cell in stateA is empty
            b) minus: A symbol exists in stateA at certain cell, but the same cell in stateB is empty
            c) diff: The same cell contains different symbols in the two states

            Returns:
                Dict[str, List[Tuple[int, int, str]]]: A dictionary with 3 key-value pairs. The key is one of the 3 difference types,
                    and the value is a list of tuples. Each tuple contains 3 items. The first 2 are the coordinates of the cell, and 
                    the last is the symbol that is different.
        '''

        result: Dict[str, List[Tuple[int, int, str]]] = {
            "plus": [],
            "minus": [],
            "diff": []
        }

        for row in range(self.dimension):
            for column in range(self.dimension):
                stateACellIsEmpty: bool = stateA.cellIsEmpty(row, column)
                stateBCellIsEmpty: bool = stateB.cellIsEmpty(row, column)

                if (stateACellIsEmpty == True and stateBCellIsEmpty == False):
                    result["plus"].append((row, column, stateB.getCellSymbol(row, column)))
                
                if (stateACellIsEmpty == False and stateBCellIsEmpty == True):
                    result["minus"].append((row, column, stateA.getCellSymbol(row, column)))

                if ((stateACellIsEmpty == False and stateBCellIsEmpty == False)):
                    if (stateA.getCellSymbol(row, column) != stateB.getCellSymbol(row, column)):
                        result["diff"].append((row, column, stateB.getCellSymbol(row, column)))

        return result
    
        