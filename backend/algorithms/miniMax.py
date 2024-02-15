from backend.components.state import State

class MiniMax:
    def __init__(self, playerA: str, playerB: str):
        self.playerA = playerA
        self.playerB = playerB
        pass

    def evaluationFunction(self, state: State, currentPlayer: str) -> int:
        '''
            Evaluates the given state based on the following formula:
                value = 3 * X2 + X1 - (3 * Y2 + Y1)

            Parameters:
                state (State): A snapshot of the game that we want to evaluate, which means to determine
                    how much beneficial is for the player currently playing
                currentPlayer (str): the symbol of the player currently playing

            Returns:
                int: How much beneficial is for the player
        '''
        X2: int = self.__calculateX2(state, currentPlayer)
        X1: int = self.__calculateX1(state, currentPlayer)
        Y2: int = self.__calculateY2(state, currentPlayer)
        Y1: int = self.__calculateY1(state, currentPlayer)

        return 3 * X2 + X1 - (3 * Y2 + Y1)


    def findOpponent(self, player: str) -> str:
        '''
            Finds the symbol that the opponent of the given player uses
        '''
        return self.playerA if (player == self.playerB) else self.playerB


    def __calculateX2(self, state: State, currentPlayer: str) -> int:
        '''
            Calculates the number of rows, columns, diagonals that contain 2 symbols of the current player
                and 0 symbols of the opponent

            Returns:
                int: The result (X2)
        '''
        opponent: str = self.findOpponent(currentPlayer)
        result: int = 0
        for row in range(state.dimension):
            if (self.__containsOnlyTwoAllySymbols(state.getRow(row), currentPlayer, opponent)):
                result += 1

        for column in range(state.dimension):
            if (self.__containsOnlyTwoAllySymbols(state.getColumn(column), currentPlayer, opponent)):
                result += 1

        if (self.__containsOnlyTwoAllySymbols(state.getPrimaryDiagonal(), currentPlayer, opponent)):
            result += 1

        if (self.__containsOnlyTwoAllySymbols(state.getSecondaryDiagonal(), currentPlayer, opponent)):
            result += 1

        return result


    def __calculateX1(self, state: State, currentPlayer: str) -> int:
        '''
            Calculates the number of rows, columns, diagonals that contain 1 symbol of the current player
                and 0 symbols of the opponent

            Returns:
                int: The result (X1)
        '''
        opponent: str = self.findOpponent(currentPlayer)
        result: int = 0
        for row in range(state.dimension):
            if (self.__containsOnlyOneAllySymbol(state.getRow(row), currentPlayer, opponent)):
                result += 1

        for column in range(state.dimension):
            if (self.__containsOnlyOneAllySymbol(state.getColumn(column), currentPlayer, opponent)):
                result += 1

        if (self.__containsOnlyOneAllySymbol(state.getPrimaryDiagonal(), currentPlayer, opponent)):
            result += 1

        if (self.__containsOnlyOneAllySymbol(state.getSecondaryDiagonal(), currentPlayer, opponent)):
            result += 1

        return result


    def __calculateY2(self, state: State, currentPlayer: str) -> int:
        '''
            Calculates the number of rows, columns, diagonals that contain 0 symbols of the current player
                and 2 symbols of the opponent

            Returns:
                int: The result (Y2)
        '''
        opponent: str = self.findOpponent(currentPlayer)
        result: int = 0
        for row in range(state.dimension):
            if (self.__containsOnlyTwoOpponentSymbols(state.getRow(row), currentPlayer, opponent)):
                result += 1

        for column in range(state.dimension):
            if (self.__containsOnlyTwoOpponentSymbols(state.getColumn(column), currentPlayer, opponent)):
                result += 1

        if (self.__containsOnlyTwoOpponentSymbols(state.getPrimaryDiagonal(), currentPlayer, opponent)):
            result += 1

        if (self.__containsOnlyTwoOpponentSymbols(state.getSecondaryDiagonal(), currentPlayer, opponent)):
            result += 1

        return result


    def __calculateY1(self, state: State, currentPlayer: str) -> int:
        '''
            Calculates the number of rows, columns, diagonals that contain 0 symbols of the current player
                and 1 symbols of the opponent

            Returns:
                int: The result (Y1)
        '''
        opponent: str = self.findOpponent(currentPlayer)
        result: int = 0
        for row in range(state.dimension):
            if (self.__containsOnlyOneOpponentSymbol(state.getRow(row), currentPlayer, opponent)):
                result += 1

        for column in range(state.dimension):
            if (self.__containsOnlyOneOpponentSymbol(state.getColumn(column), currentPlayer, opponent)):
                result += 1

        if (self.__containsOnlyOneOpponentSymbol(state.getPrimaryDiagonal(), currentPlayer, opponent)):
            result += 1

        if (self.__containsOnlyOneOpponentSymbol(state.getSecondaryDiagonal(), currentPlayer, opponent)):
            result += 1

        return result

    
    def __containsOnlyTwoAllySymbols(self, symbols: list[str], currentPlayer: str, opponent: str) -> bool:
        '''
            Checks if the given list of {symbols} includes exactly 2 symbols of the {currentPlayer}
                and 0 symbols of his {opponent}
            
            Parameters:
                currentPlayer (str): The symbol of the player that currently plays
                opponent (str): The symbol of the other player

            Returns:
                bool: True/False based on this condition
        '''
        totalAllySymbolAppearances = self.__calculateTotalAppearances(symbols, currentPlayer)
        totalOpponentSymbolAppearances = self.__calculateTotalAppearances(symbols, opponent)

        return totalAllySymbolAppearances == 2 and totalOpponentSymbolAppearances == 0


    def __containsOnlyOneAllySymbol(self, symbols: list[str], currentPlayer: str, opponent: str) -> bool:
        '''
            Checks if the given list of {symbols} includes exactly 1 symbol of the {currentPlayer}
                and 0 symbols of his {opponent}
            
            Parameters:
                currentPlayer (str): The symbol of the player that currently plays
                opponent (str): The symbol of the other player

            Returns:
                bool: True/False based on this condition
        '''
        totalAllySymbolAppearances = self.__calculateTotalAppearances(symbols, currentPlayer)
        totalOpponentSymbolAppearances = self.__calculateTotalAppearances(symbols, opponent)

        return totalAllySymbolAppearances == 1 and totalOpponentSymbolAppearances == 0
    

    def __containsOnlyTwoOpponentSymbols(self, symbols: list[str], currentPlayer: str, opponent: str) -> bool:
        '''
            Checks if the given list of {symbols} includes exactly 0 symbols of the {currentPlayer}
                and 2 symbols of his {opponent}
            
            Parameters:
                currentPlayer (str): The symbol of the player that currently plays
                opponent (str): The symbol of the other player

            Returns:
                bool: True/False based on this condition
        '''
        totalAllySymbolAppearances = self.__calculateTotalAppearances(symbols, currentPlayer)
        totalOpponentSymbolAppearances = self.__calculateTotalAppearances(symbols, opponent)

        return totalAllySymbolAppearances == 0 and totalOpponentSymbolAppearances == 2


    def __containsOnlyOneOpponentSymbol(self, symbols: list[str], currentPlayer: str, opponent) -> bool:
        '''
            Checks if the given list of {symbols} includes exactly 0 symbols of the {currentPlayer}
                and 1 symbol of his {opponent}
            
            Parameters:
                currentPlayer (str): The symbol of the player that currently plays
                opponent (str): The symbol of the other player

            Returns:
                bool: True/False based on this condition
        '''
        totalAllySymbolAppearances = self.__calculateTotalAppearances(symbols, currentPlayer)
        totalOpponentSymbolAppearances = self.__calculateTotalAppearances(symbols, opponent)

        return totalAllySymbolAppearances == 0 and totalOpponentSymbolAppearances == 1
    

    def __calculateTotalAppearances(self, symbols: list[str], symbol: str) -> int:
        '''
            Calculates how many times the given {symbol} is appeared inside the {symbols} list

            Parameters:
                symbols (list[str]): A list containing symbols. It represents a row, a column or a diagonal
                symbol (str): A character that a player uses or the ' '


            Returns:
                int: The result
        '''
        result: int = 0
        for s in symbols:
            if (s == symbol):
                result += 1
        
        return result


    
