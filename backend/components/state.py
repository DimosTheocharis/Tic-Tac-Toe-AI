class State:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.createGrid()

    def createGrid(self) -> None:
        self.grid = [[' ' for j in range(self.dimension)] for i in range(self.dimension)]

    def assignGrid(self, grid: list[list[str]]):
        self.grid = grid


    def printGrid(self) -> None:
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
        if (row >= self.dimension or column >= self.dimension):
            print("Coordinates out of limit.")
            return False
        
        if (self.grid[row][column] != " "):
            print("Place already occupied.")
            return False
        
        self.grid[row][column] = symbol

        return True
            
            