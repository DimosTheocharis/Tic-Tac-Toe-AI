from backend.components.state import State

class Game:
    def __init__(self):
        self.dimension = 3
        self.game = State(self.dimension)

    def isVictory(self) -> None:
        for i in range(self.dimension):
            if (self.checkRow(i)):
                print(f"The row {i} makes Tic-Tac-Toe!")

        for j in range(self.dimension):
            if (self.checkColumn(j)):
                print(f"The column {j} makes Tic-Tac-Toe!")

        if (self.checkPrimaryDiagonal()):
            print("The primary diagonal makes Tic-Tac-Toe!")

        if (self.checkSecondaryDiagonal()):
            print("The secondary diagonal makes Tic-Tac-Toe!")

    def checkRow(self, row: int) -> bool: 
        match: bool = True
        j: int = 0
        while (match and j < self.dimension - 1):
            match = self.game.grid[row][j] == self.game.grid[row][j + 1]
            j += 1

        return match 

    def checkColumn(self, column: int) -> bool: 
        match: bool = True
        i: int = 0
        while (match and i < self.dimension - 1):
            match = self.game.grid[i][column] == self.game.grid[i + 1][column]
            i += 1

        return match 

    def checkPrimaryDiagonal(self) -> bool:
        match: bool = True
        x: int = 0
        while (match and x < self.dimension - 1):
            match = self.game.grid[x][x] == self.game.grid[x + 1][x + 1]
            x += 1

        return match

    def checkSecondaryDiagonal(self) -> bool:
        match: bool = True
        x: int = self.dimension - 1
        while (match and x > 0):
            match = self.game.grid[x][self.dimension - 1 - x] == self.game.grid[x - 1][self.dimension - x]
            x -= 1

        return match
        