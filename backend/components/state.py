class State:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.createGrid()

    def createGrid(self) -> None:
        '''
            Creates a self.dimension X self.dimension grid and fills its cells with ' '
        '''
        self.grid = [[' ' for j in range(self.dimension)] for i in range(self.dimension)]


    def assignGrid(self, grid: list[list[str]]):
        '''
            Assigns the grid that gets as parameter to self.grid
        '''
        self.grid = grid


    def printGrid(self) -> None:
        '''
            Prints in console a visual representation of the grid. For example

            O|X|X

            X|O|X

            O|O|O

        '''
        for i in range(self.dimension - 1):
            for j in range(self.dimension - 1):
                print(self.grid[i][j], end='')
                print("|", end='')
            print(self.grid[i][self.dimension - 1])
            for j in range(2 * self.dimension - 1):
                print("-", end='')
            print()
        
        for j in range(self.dimension - 1):
            print(self.grid[self.dimension - 1][j], end='')
            print("|", end='')
        print(self.grid[self.dimension - 1][self.dimension - 1])


    def play(self, symbol: str, row: int, column: int) -> bool:
        '''
            Implements the move of a player in given coordinates. If dimensions are out of limit or the corresponding 
            cell is already filled, then logs a relative message and returns.

            Parameters:
                symbol (str): A character that is related to the player playing
                row (int): The row of the grid that contains the cell where the symbol is going to be placed
                column (int): The column of the grid that contains the cell where the symbol is going to be placed

            Returns:
                bool: True if the move executed successfully, False otherwise
        '''
        if (row >= self.dimension or column >= self.dimension):
            print("Coordinates out of limit.")
            return False
        
        if (self.grid[row][column] != " "):
            print("Place already occupied.")
            return False
        
        self.grid[row][column] = symbol

        return True
    

    def isVictory(self) -> bool:
        '''
            Checks if one of the 2 players has won the game
        '''
        for i in range(self.dimension):
            if (self.__checkRow(i)):
                return True

        for j in range(self.dimension):
            if (self.__checkColumn(j)):
                return True

        if (self.__checkPrimaryDiagonal()):
            return True

        if (self.__checkSecondaryDiagonal()):
            return True


    def __checkRow(self, row: int) -> bool: 
        '''
            Checks if the row at index {row} wins the game (contains 3 consecutive same symbols)

            Returns: 
                bool: True for victory, False otherwise
        '''
        match: bool = self.grid[row][0] != " "
        j: int = 0
        while (match and j < self.dimension - 1):
            match = self.grid[row][j] == self.grid[row][j + 1]
            j += 1

        return match 


    def __checkColumn(self, column: int) -> bool: 
        '''
            Checks if the column at index {column} wins the game (contains 3 consecutive same symbols)

            Returns: 
                bool: True for victory, False otherwise
        '''
        match: bool = self.grid[0][column] != " "
        i: int = 0
        while (match and i < self.dimension - 1):
            match = self.grid[i][column] == self.grid[i + 1][column]
            i += 1

        return match 


    def __checkPrimaryDiagonal(self) -> bool:
        '''
            Checks if the primary diagonal wins the game (contains 3 consecutive same symbols

            Returns: 
                bool: True for victory, False otherwise
        '''
        match: bool = self.grid[0][0] != " "
        x: int = 0
        while (match and x < self.dimension - 1):
            match = self.grid[x][x] == self.grid[x + 1][x + 1]
            x += 1

        return match

    
    def __checkSecondaryDiagonal(self) -> bool:
        '''
            Checks if the secondary diagonal wins the game (contains 3 consecutive same symbols).
            
            Returns: 
                bool: True for victory, False otherwise
        '''
        match: bool = self.grid[0][self.dimension - 1] != " "
        x: int = self.dimension - 1
        while (match and x > 0):
            match = self.grid[x][self.dimension - 1 - x] == self.grid[x - 1][self.dimension - x]
            x -= 1

        return match

    
    def gridIsFull(self) -> bool:
        '''
            Checks if the grid is full of symbols, which means the game has ended.

            Returns:
                bool: True if grid is full, False otherwise
        '''
        for row in self.grid:
            for cell in row:
                if cell == ' ':
                    return False

        return True

            
            