from typing import Tuple
from enum import Enum

from backend.game import Game, PlayerMoveResponse

class GameStatus(Enum):
    '''
        Running: The game is running without any problem. 
        Ended: The game has ended. Neither human nor compute can play. 
        Idle: The game is waiting for the algorithm to make his move.
    '''
    RUNNING = 1
    ENDED = 2
    IDLE = 3

class CurrentPlayer(Enum):
    HUMAN = 1
    COMPUTER = 2


class Middleman:
    def __init__(self):
        self.__game: Game = Game()
        self.gameStatus: GameStatus = GameStatus(GameStatus.RUNNING)
        self.currentPlayer: CurrentPlayer = CurrentPlayer(CurrentPlayer.HUMAN)


    def humanWillPlay(self, coordinates: Tuple[int, int]) -> str:
        '''
            Requests from the backend to let the human player make his move in the cell at the given {coordinates}
            of the grid. This will happen only if the game is still running, and if it's player's turn to play.

            Returns: 
                str: A message about the response of the backend or a message giving information about the failure of the move.
        '''
        if (self.gameStatus.name == "ENDED"):
            return "Game has ended.."


        if (self.currentPlayer == CurrentPlayer.HUMAN):
            response: PlayerMoveResponse = self.__game.humanRequestsToPlayFromFrontend(coordinates)

            if (response.successful):
                self.currentPlayer = CurrentPlayer.COMPUTER

            if (response.gameHasEnded):
                self.gameStatus = GameStatus.ENDED

            return response.message
        
        else:
            return "Is not your turn to play..."
    

    
    def computerWillPlay(self) -> str:
        '''
            Requests from the backend to let the algorithm make his move, based on the current state of the grid.
            This will happen only if the game is still running, and if it's computer's turn to play.  

            Returns:
                A message based on the action
        '''
        if (self.gameStatus.name == "ENDED"):
            return "Game has ended.."
        
        if (self.gameStatus.name == "IDLE"):
            return "Waiting for the computer to play..."
        

        if (self.currentPlayer == CurrentPlayer.COMPUTER and self.gameStatus.name == "RUNNING"):
            self.gameStatus = GameStatus.IDLE
            response: PlayerMoveResponse = self.__game.computerRequestsToPlayFromFrontend()

            self.gameStatus = GameStatus.RUNNING

            if (response.successful):
                self.currentPlayer = CurrentPlayer.HUMAN

            if (response.gameHasEnded):
                self.gameStatus = GameStatus.ENDED

            return response.message
        
        else:
            return ""
        


    def getCellSymbol(self, row: int, column: int) -> str:
        '''
            Requests from the game object to access the cell in coordinates ({row}, {column}) in order
            to get the symbol in that cell.
        '''

        return self.__game.getCellSymbol(row, column)
    

    def checkIfRowWins(self, row: int) -> bool: 
        '''
            Checks if the given {row} of the grid of the current game performs tic-tac-toe.
        '''
        if (row < 0 or row >= self.__game.getDimension()):
            return False

        match row:
            case 0:
                return self.__game.checkIfRowWins(0)
            case 1:
                return self.__game.checkIfRowWins(1)
            case 2:
                return self.__game.checkIfRowWins(2)
            

    def checkIfColumnWins(self, column: int) -> bool: 
        '''
            Checks if the given {column} of the grid of the current game performs tic-tac-toe.
        '''
        if (column < 0 or column >= self.__game.getDimension()):
            return False

        match column:
            case 0:
                return self.__game.checkIfColumnWins(0)
            case 1:
                return self.__game.checkIfColumnWins(1)
            case 2:
                return self.__game.checkIfColumnWins(2)
            

    def checkIfPrimaryDiagonalWins(self) -> bool:
        '''
            Checks if the primary diagonal of the grid of the current game performs tic-tac-toe.
        '''
        return self.__game.checkIfPrimaryDiagonalWins()
    
    
    def checkIfSecondaryDiagonalWins(self) -> bool:
        '''
            Checks if the secondary diagonal of the grid of the current game performs tic-tac-toe.
        '''
        return self.__game.checkIfSecondaryDiagonalWins()
    