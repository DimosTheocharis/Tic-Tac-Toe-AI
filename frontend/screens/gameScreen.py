from typing import Tuple

import pygame
from pygame import Surface

from backend.components.state import State
from screens.generalScreen import GeneralScreen
from backend.game import Game
from styles.generalStyles import Colors, Fonts



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
        self.__panelBackgroundColor = Colors["slateGrey"]
        self.__oddCellColor = Colors["deepBlue"]
        self.__evenCellColor = Colors["petrol"]
    

    def display(self, window: Surface, events) -> None:
        self.drawGrid(window)
        self.__drawInformerPanel(window)

        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN):
                x, y = pygame.mouse.get_pos()

                row: int = y // self.__cellHeight
                column: int = x // self.__cellWidth



    def drawGrid(self, window: Surface):
        '''
            This method is responsible for drawing the Tic-Tac-Toe grid
        '''
        self.__drawCells(window)

        self.__drawGridBorder(window)

        self.__drawHorizontalLines(window)

        self.__drawVerticalLines(window)

        self.__drawSymbols(window)

    
    def __drawCells(self, window: Surface) -> None:
        '''
            Draws the cells of the tic-tac-toe grid in alternate colors
        '''
        for row in range(self.__dimension):
            for column in range(self.__dimension):
                index: int = row * self.__dimension + column + 1
                color: Tuple[int, int, int] = self.__oddCellColor if index % 2 == 1 else self.__evenCellColor
                
                positionX: int = column * self.__cellWidth
                positionY: int = row * self.__cellHeight

                pygame.draw.rect(window, color, (positionX, positionY, self.__cellWidth, self.__cellHeight))



    def __drawGridBorder(self, window: Surface) -> None:
        '''
            Draws a border around of the tic-tac-toe grid 
        '''
        offset: int = self.__lineThickness // 2

        pygame.draw.line(window, self.__lineColor, (0, 0 + offset), (self.__width, 0 + offset), self.__lineThickness)
        pygame.draw.line(window, self.__lineColor, (self.__width - offset, 0), (self.__width - offset, self.__height), self.__lineThickness)
        pygame.draw.line(window, self.__lineColor, (self.__width, self.__height - offset), (0, self.__height - offset), self.__lineThickness)
        pygame.draw.line(window, self.__lineColor, (0 + offset, self.__height), (0 + offset, 0), self.__lineThickness)


    def __drawHorizontalLines(self, window: Surface) -> None:
        '''
            Draws the horizontal lines of the tic-tac-toe grid
        '''
        for i in range(self.__dimension - 1):
            lineHeight: int = (i + 1) * self.__cellHeight
            pygame.draw.line(window, self.__lineColor, (0, lineHeight), (self.__width, lineHeight), self.__lineThickness)


    def __drawVerticalLines(self, window: Surface) -> None:
        '''
            Draws the vertical lines of the tic-tac-toe grid
        '''
        for i in range(self.__dimension - 1):
            lineWidth: int = (i + 1) * self.__cellWidth
            pygame.draw.line(window, self.__lineColor, (lineWidth, 0), (lineWidth, self.__height), self.__lineThickness)


    
    def __drawSymbols(self, window: Surface) -> None:
        '''
            Draws the symbols of the current tic-tac-game in the corresponding positions
        '''
        state: State = self.__game.getState()
        for row in range(self.__dimension):
            for column in range(self.__dimension):
                symbolSurface: Surface = self.__symbolFont.render(state.getCellSymbol(row, column), False, self.__symbolForegroundColor)

                positionX: int = (column) * self.__cellWidth + (self.__cellWidth // 2 - symbolSurface.get_width() // 2)
                positionY: int = (row) * self.__cellHeight + (self.__cellHeight // 2 - symbolSurface.get_height() // 2)

                window.blit(symbolSurface, (positionX, positionY))

    
    def __drawInformerPanel(self, window: Surface):
        '''
            This method is responsible for drawing a small window under the grid that informs the player about 
            the state of the game.
        '''
        pygame.draw.rect(window, self.__panelBackgroundColor, (0, self.__height, self.__width, 100))