import pygame
from pygame import Surface
from backend.components.state import State

from screens.generalScreen import GeneralScreen
from backend.game import Game
from styles.general import Colors, Fonts



class GameScreen(GeneralScreen):
    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height    
        self.__dimension = 3
        self.__cellWidth = self.__width // self.__dimension
        self.__cellHeight = self.__height // self.__dimension

        self.__game: Game = Game()

        self.__defineStyleVariables()


    def __defineStyleVariables(self):
        self.__lineThickness = 15
        self.__lineColor = Colors["black"]
        self.__symbolFont = Fonts["verdana"]
        self.__symbolForegroundColor = Colors["black"]
    

    def display(self, window: Surface) -> None:
        self.drawGrid(window)


    def drawGrid(self, window: Surface):
        '''
            This method is responsible for drawing the Tic-Tac-Toe grid
        '''
        # Draw grid border
        offset: int = self.__lineThickness // 2

        pygame.draw.line(window, self.__lineColor, (0, 0 + offset), (self.__width, 0 + offset), self.__lineThickness)
        pygame.draw.line(window, self.__lineColor, (self.__width - offset, 0), (self.__width - offset, self.__height), self.__lineThickness)
        pygame.draw.line(window, self.__lineColor, (self.__width, self.__height - offset), (0, self.__height - offset), self.__lineThickness)
        pygame.draw.line(window, self.__lineColor, (0 + offset, self.__height), (0 + offset, 0), self.__lineThickness)

        # Draw horizontal lines
        for i in range(self.__dimension - 1):
            lineHeight: int = (i + 1) * self.__cellHeight
            pygame.draw.line(window, self.__lineColor, (0, lineHeight), (self.__width, lineHeight), self.__lineThickness)


        # Draw vertical lines
        for i in range(self.__dimension - 1):
            lineWidth: int = (i + 1) * self.__cellWidth
            pygame.draw.line(window, self.__lineColor, (lineWidth, 0), (lineWidth, self.__height), self.__lineThickness)

        
        # Draw symbols
        state: State = self.__game.getState()
        for row in range(self.__dimension):
            for column in range(self.__dimension):
                symbolSurface: Surface = self.__symbolFont.render(state.getCellSymbol(row, column), False, self.__symbolForegroundColor)

                positionX: int = (column) * self.__cellWidth + (self.__cellWidth // 2 - symbolSurface.get_width() // 2)
                positionY: int = (row) * self.__cellHeight + (self.__cellHeight // 2 - symbolSurface.get_height() // 2)


                window.blit(symbolSurface, (positionX, positionY))





