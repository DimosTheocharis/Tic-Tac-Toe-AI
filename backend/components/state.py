from __future__ import annotations

class State():
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.__createGrid()

    def __createGrid(self) -> None:
        '''
            Creates a self.dimension X self.dimension grid and fills its cells with ' '
        '''
        self.__grid: list[list[str]] = [[' ' for j in range(self.dimension)] for i in range(self.dimension)]


    def assignGrid(self, grid: list[list[str]]):
        '''
            Assign a copy of the grid that gets as parameter to self.__grid
        '''
        self.__grid = [[grid[row][column] for column in range(self.dimension)] for row in range(self.dimension)]


    def printGrid(self) -> None:
        '''
            Prints in console a visual representation of the grid. For example

               0 1 2
              -------
            0 |O|X|X| 
              |-----| 
            1 |X|O|X|
              |-----|
            2 |O|O|O|
              -------

        '''
        # Print column indicators
        print("   ", end='')
        for i in range(self.dimension):
            print(i, end='')
            print(' ', end='')
        print()

        # Print top edge ('-------')
        print("  ", end='')
        for i in range(2 * self.dimension + 1):
            print("-", end='')
        print()

        # Print first {self.dimension - 1} lines with seperator line ('|-----|') under them 
        for i in range(self.dimension - 1):
            # Print row indicator
            print(i, end='')
            print(' ', end='')

            # Print left edge part ('|')
            print('|', end='')

            # Print the symbol of the cell, and a '|' column seperator after
            for j in range(self.dimension - 1):
                print(self.__grid[i][j], end='')
                print("|", end='')

            # Print last symbol of the row
            print(self.__grid[i][self.dimension - 1], end='')

            # Print right edge part ('|')
            print('|')

            # Print seperator line ('|-----|')
            print("  ", end='')
            print('|', end='')
            for j in range(2 * self.dimension - 1):
                print("-", end='')
            print('|', end='')
            print()
        
        # Print last line, without extra seperator line ('|-----|') under them
        print(self.dimension - 1, end='')
        print(' ', end='')
        print('|', end='') 
        for j in range(self.dimension - 1):
            print(self.__grid[self.dimension - 1][j], end='')
            print("|", end='')
        print(self.__grid[self.dimension - 1][self.dimension - 1], end='')
        print('|')

        # Print bottom edge ('-------')
        print("  ", end='')
        for i in range(2 * self.dimension + 1):
            print("-", end='')
        print()


    def play(self, symbol: str, row: int, column: int) -> None:
        '''
            Implements the move of a player in given coordinates. The coordinates must be checked before entering this function!

            Parameters:
                symbol (str): A character that is related to the player playing
                row (int): The row of the grid that contains the cell where the symbol is going to be placed
                column (int): The column of the grid that contains the cell where the symbol is going to be placed
        '''
        
        self.__grid[row][column] = symbol
    

    def isVictory(self) -> bool:
        '''
            Checks if one of the 2 players has won the game
        '''
        for i in range(self.dimension):
            if (self.checkRow(i)):
                return True

        for j in range(self.dimension):
            if (self.checkColumn(j)):
                return True

        if (self.checkPrimaryDiagonal()):
            return True

        if (self.checkSecondaryDiagonal()):
            return True


    def checkRow(self, row: int) -> bool: 
        '''
            Checks if the row at index {row} wins the game (contains 3 consecutive same symbols)

            Returns: 
                bool: True for victory, False otherwise
        '''
        match: bool = self.__grid[row][0] != " "
        j: int = 0
        while (match and j < self.dimension - 1):
            match = self.__grid[row][j] == self.__grid[row][j + 1]
            j += 1

        return match 


    def checkColumn(self, column: int) -> bool: 
        '''
            Checks if the column at index {column} wins the game (contains 3 consecutive same symbols)

            Returns: 
                bool: True for victory, False otherwise
        '''
        match: bool = self.__grid[0][column] != " "
        i: int = 0
        while (match and i < self.dimension - 1):
            match = self.__grid[i][column] == self.__grid[i + 1][column]
            i += 1

        return match 


    def checkPrimaryDiagonal(self) -> bool:
        '''
            Checks if the primary diagonal wins the game (contains 3 consecutive same symbols

            Returns: 
                bool: True for victory, False otherwise
        '''
        match: bool = self.__grid[0][0] != " "
        x: int = 0
        while (match and x < self.dimension - 1):
            match = self.__grid[x][x] == self.__grid[x + 1][x + 1]
            x += 1

        return match

    
    def checkSecondaryDiagonal(self) -> bool:
        '''
            Checks if the secondary diagonal wins the game (contains 3 consecutive same symbols).
            
            Returns: 
                bool: True for victory, False otherwise
        '''
        match: bool = self.__grid[0][self.dimension - 1] != " "
        x: int = self.dimension - 1
        while (match and x > 0):
            match = self.__grid[x][self.dimension - 1 - x] == self.__grid[x - 1][self.dimension - x]
            x -= 1

        return match

    
    def gridIsFull(self) -> bool:
        '''
            Checks if the grid is full of symbols, which means the game has ended.

            Returns:
                bool: True if grid is full, False otherwise
        '''
        for row in self.__grid:
            for cell in row:
                if cell == ' ':
                    return False

        return True
    

    def getRow(self, row: int) -> list[str]:
        '''
            Returns a list with the elements of the row at position {row} of the grid, 
            ie the elements [row][0], [row][1] etc
        '''
        if (row < 0 or row >= self.dimension):
            return []
        return self.__grid[row]
    
    
    def getColumn(self, column: int) -> list[str]:
        '''
            Returns a list with the elements of the column at position {column} of the grid, 
            ie the elements [0][column], [1][column] etc
        '''
        if (column < 0 or column >= self.dimension):
            return []
        return [self.__grid[j][column] for j in range(self.dimension)]
    
    
    def getPrimaryDiagonal(self) -> list[str]:
        '''
            Returns a list with the elements of the primary diagonal of the grid,
            ie the elements [0][0], [1][1] etc
        '''
        return [self.__grid[x][x] for x in range(self.dimension)]
    

    def getSecondaryDiagonal(self) -> list[str]:
        '''
            Returns a list with the elements of the secondary diagonal of the grid,
            ie the elements [2][0], [1][1] etc (for self.dimension = 3)
        '''
        return [self.__grid[self.dimension - 1 - x][x] for x in range(self.dimension)]
    
    
    def getChildStates(self, symbol: str) -> list[State]:
        '''
            Creates all possible states of tic-tac-toe game that can occur after the player 
            currently playing make his move

            Parameters:
                symbol (str): The symbol that the player who is currently playing uses

            Returns: 
                list[State]: A list with all these child states
        '''
        result: list[State] = []

        emptyCellCoordinates: list[tuple[int, int]] = self.__getEmptyCellCoordinates()
        for coordinates in emptyCellCoordinates:
            child: State = State(self.dimension)
            child.assignGrid(self.__grid)

            child.setCellSymbol(coordinates[0], coordinates[1], symbol)

            result.append(child)

        return result

    
            
    def __getEmptyCellCoordinates(self) -> list[tuple[int, int]]:
        '''
            Finds and returns a list with (row, column) coordinates where grid[row][column] is empty
        '''
        result: list[tuple[int, int]] = []
        for row in range(self.dimension):
            for column in range(self.dimension):
                if (self.__grid[row][column] == ' '):
                    result.append((row, column))

        return result
    

    def getCellSymbol(self, row: int, column: int) -> str:
        '''
            Returns the symbol that is contained inside grid, at the given {row}, {column} coordinates.
            If coordinates are out of limit, then returns None
        '''
        if (row < 0 or row >= self.dimension or column < 0 or column >= self.dimension):
            print(f"Coordinates ({row},{column}) are out of limit!")
            return None
        
        return self.__grid[row][column]
    

    def setCellSymbol(self, row: int, column: int, symbol: str) -> None:
        '''
            Set the given {symbol} at the given {row}, {column} coordinates
            If coordinates are out of limit, then returns None
        '''
        if (row < 0 or row >= self.dimension or column < 0 or column >= self.dimension):
            print(f"Coordinates ({row},{column}) are out of limit!")
            return None
        
        self.__grid[row][column] = symbol
    

    def cellIsEmpty(self, row: int, column: int) -> bool:
        '''
            Returns true if cell is empty, false otherwise.
        '''
        symbol: str = self.getCellSymbol(row, column)
        if (symbol == None):
            return None
        
        return symbol == ' '