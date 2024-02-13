from backend.components.state import State

class MiniMax:
    def __init__():
        a = 4

    def evaluationFunction(self, state: State) -> int:
        '''
            Evaluates the given state based on the following formula:
                value = 3 * X2 + X1 - (3 * Y2 + Y1)

            Parameters:
                state (State): A snapshot of the game that we want to evaluate, which means to determine
                    how much beneficial is for the player currently playing

            Returns:
                int: How much beneficial is for the player
        '''
        pass

    def __calculateX2(self) -> int:
        '''
            Calculates the number of rows, columns, diagonals that contain 2 symbols of the current player
                and 0 symbols of the opponent

            Returns:
                int: The result (X2)
        '''
        pass


    def __calculateX1(self) -> int:
        '''
            Calculates the number of rows, columns, diagonals that contain 1 symbol of the current player
                and 0 symbols of the opponent

            Returns:
                int: The result (X1)
        '''
        pass


    def __calculateY2(self) -> int:
        '''
            Calculates the number of rows, columns, diagonals that contain 0 symbols of the current player
                and 2 symbols of the opponent

            Returns:
                int: The result (Y2)
        '''
        pass


    def __calculateY1(self) -> int:
        '''
            Calculates the number of rows, columns, diagonals that contain 0 symbols of the current player
                and 1 symbols of the opponent

            Returns:
                int: The result (Y1)
        '''
        pass

    
    def __containsOnlyTwoAllySymbols(self, symbols: list[int], currentPlayer: str) -> bool:
        '''
            Checks if the given list of symbols includes exactly 2 symbols of the {currentPlayer}
                and 0 symbols of his opponent
            
            Parameters:
                currentPlayer (int): The symbol of the player that currently plays

            Returns:
                bool: True/False based on this condition
        '''
        pass


    def __containsOnlyOneAllySymbol(self, symbols: list[int], currentPlayer: str) -> bool:
        '''
            Checks if the given list of symbols includes exactly 1 symbol of the {currentPlayer}
                and 0 symbols of his opponent
            
            Parameters:
                currentPlayer (int): The symbol of the player that currently plays

            Returns:
                bool: True/False based on this condition
        '''
        pass


    def __containsOnlyTwoOpponentSymbols(self, symbols: list[int], currentPlayer: str) -> bool:
        '''
            Checks if the given list of symbols includes exactly 0 symbols of the {currentPlayer}
                and 2 symbols of his opponent
            
            Parameters:
                currentPlayer (int): The symbol of the player that currently plays

            Returns:
                bool: True/False based on this condition
        '''
        pass


    def __containsOnlyOneOpponentSymbol(self, symbols: list[int], currentPlayer: str) -> bool:
        '''
            Checks if the given list of symbols includes exactly 0 symbols of the {currentPlayer}
                and 1 symbol of his opponent
            
            Parameters:
                currentPlayer (int): The symbol of the player that currently plays

            Returns:
                bool: True/False based on this condition
        '''
        pass


    def __calculateTotalAppearances(self, symbols: list[int], symbol: str) -> int:
        '''
            Calculates how many times the given {symbol} is appeared inside the {symbols} list

            Parameters:
                symbols (list[int]): A list containing symbols (the symbols of the 2 players and possibly the ' ' symbol). It
                    represents a row, a column or a diagonal


            Returns:
                int: The result
        '''
        pass


    

