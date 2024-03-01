from typing import Tuple

from backend.game import Game, PlayerMoveResponse


class Middleman:
    def __init__(self):
        self.__game: Game = Game()

    def play(self, coordinates: Tuple[int, int]) -> str:
        response: PlayerMoveResponse = self.__game.playFromFrontend(coordinates)

        return response.message
    
    def playAlgorithm(self) -> str:
        '''
            Requests from algorithm to make his move

            Returns:
                A message based on the action
        '''
        response: PlayerMoveResponse = self.__game.requestAlgorithmMove()

        return response.message

    def getCellSymbol(self, row: int, column: int) -> str:
        '''
            Requests from the game object to access the cell in coordinates ({row}, {column}) in order
            to get the symbol in that cell.
        '''

        return self.__game.getCellSymbol(row, column)