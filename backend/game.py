from typing import Dict, List, Tuple

from components.state import State
from algorithms.miniMax import MiniMax

class PlayerMoveResponse:
    def __init__(self, successful: bool, message: str):
        self.successful: bool = successful
        self.message: str = message

class Game:
    def __init__(self):
        self.__dimension: int = 3
        self.__playerA: str = "X"
        self.__playerB: str = "O"  
        self.__currentPlayer: str = self.__playerA
        self.__computerIsPlaying: bool = False
        self.__miniMax: MiniMax = MiniMax(self.__playerA, self.__playerB)
        self.__state = State(self.__dimension)
        self.__state.assignGrid([
            ['X', ' ', 'Y'],
            [' ', 'X', 'Y'],
            [' ', ' ', 'X']
        ])

    def newTerminalGame(self):
        '''
            Starts a new Tic-Tac-toe game in terminal.
        '''
        self.__state = State(self.__dimension)
        while (not (self.__state.isVictory() or self.__state.gridIsFull())):
            self.__state.printGrid()
            print("")

            if (self.__computerIsPlaying):
                nextState: State = self.__miniMax.miniMax(self.__state, 8, self.__currentPlayer)

                stateDifference: Dict[str, List[Tuple[int, int, str]]] = self.findDifferencesBetweenStates(self.__state, nextState)

                if (len(stateDifference["plus"]) == 1 and len(stateDifference["minus"]) == 0 and len(stateDifference["diff"]) == 0):
                    coordinates: tuple[int, int] = (stateDifference["plus"][0][0], stateDifference["plus"][0][1])
                    self.__state.play(self.__currentPlayer, coordinates[0], coordinates[1])
                    print(f"Computer placed {self.__currentPlayer} in (row, column) = ({coordinates[0]},{coordinates[1]})")
                else:
                    print("Computed failed to play. You may play again.")
                    break

            else:
                stop: bool = False
                while (not stop):
                    coordinates: tuple[int, int] = self.__receivePlayerInput()

                    if (self.__coordinatesOutOfLimit(coordinates)):
                        print("Coordinates out of limit. Try again: ")
                    elif (self.__cellAlreadyOccupied(coordinates)):
                        print("Place already occupied. Try again: ")
                    else:
                        self.__state.play(self.__currentPlayer, coordinates[0], coordinates[1])
                        stop = True

                
            self.__switchTurn()
            print("")

        self.__state.printGrid()
        if (self.__state.isVictory()):
            self.__switchTurn()
            print(f"Player {self.__currentPlayer} wins!")
        else:
            print("The game results to tie!")


    def getPlayerCoordinatesByFrontend(self, coordinates: Tuple[int, int]) -> PlayerMoveResponse:
        successful: bool = self.__state.play(self.__currentPlayer, coordinates[0], coordinates[1])

        if (successful):
            return PlayerMoveResponse(successful, "Something went wrong")
        else:
            return PlayerMoveResponse()
        

    def __coordinatesOutOfLimit(self, coordinates: Tuple[int, int]) -> bool:
        '''
            Checks if the given coordinates are out of limit. The coordinates are out of limit if they are 
            negative or larger than the dimension of the grid

            Parameters:
                coordinates (Tuple[int, int]): (row, column) positions
        '''
        return coordinates[0] < 0 or coordinates[0] >= self.__dimension or coordinates[1] < 0 or coordinates[1] >= self.__dimension
    

    def __cellAlreadyOccupied(self, coordinates: Tuple[int, int]) -> bool:
        '''
            Checks if the cell of the state in the given {coordinates} contains a non-empty symbol.

            Parameters:
                coordinates (Tuple[int, int]): (row, column) positions
        '''
        symbol: str = self.__state.getCellSymbol(coordinates[0], coordinates[1])

        return symbol != ' '

    


    # def newFrontendGame(self):
    #     '''
    #         Starts a new Tic-Tac-toe game that interacts with players input in frontend with the help of 
    #         python generators
    #     '''
    #     # Initiliaze a new state for the new game
    #     self.__state = State(self.__dimension)

    #     while(True):
    #         # Get the coordinates of the cell where the player who is currently playing, wants to place his symbol
    #         coordinates: tuple[int, int] = yield 

    #         if (coordinates == None):
    #             continue


    #         if (not self.__computerIsPlaying):
    #             while(not self.__state.play(self.__currentPlayer, coordinates[0], coordinates[1])):
    #                 print("Please try again:")
    #                 coordinates = yield 
    #                 print(f"--> {coordinates}")

            






    def __switchTurn(self) -> None:
        '''
            Handles the switching of the player playing.
        '''
        self.__currentPlayer = self.__playerB if self.__currentPlayer == self.__playerA else self.__playerA
        self.__computerIsPlaying = not self.__computerIsPlaying


    def __receivePlayerInput(self) -> tuple[int, int]:
        '''
            Asks current player to give the coordinates (row, column) of the cell where we wants to place his symbol

            Returns:
                tuple[int, int]: the (row, column) coordinates of the cell
        '''
        print(f"Player {self.__currentPlayer} is playing. Where do you wanna play?")

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

                For example:
                    {
                        'plus': [(2, 1, 'O')], 
                        'minus': [(1, 1, 'O')], 
                        'diff': [(0, 0, 'O'), (0, 2, 'X')]
                    }

                    means:

                    - The stateB has symbol 'O' at coordinates: (row, column) = (2, 1) but the stateA has no symbol at the same cell
                    - The stateA has symbol 'O' at coordinates: (row, column) = (1, 1) but the stateB has no symbol at the same cell
                    - The stateB has symbol 'O' at coordinates: (row, column) = (0, 0) but the stateA has symbol 'X' at the same cell
                    - The stateB has symbol 'X' at coordinates: (row, column) = (0, 2) but the stateA has symbol 'O' at the same cell


        '''

        result: Dict[str, List[Tuple[int, int, str]]] = {
            "plus": [],
            "minus": [],
            "diff": []
        }

        for row in range(self.__dimension):
            for column in range(self.__dimension):
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
    
    def getState(self) -> State:
        return self.__state
        