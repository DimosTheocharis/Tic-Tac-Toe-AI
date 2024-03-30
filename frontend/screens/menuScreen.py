from typing import Tuple, List

import pygame
from pygame import Surface, Rect
from pygame.event import Event

from frontend.styles.generalStyles import Colors, Fonts
from screens.generalScreen import GeneralScreen
from components.button import Button

class MenuScreen(GeneralScreen):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        self.__cellWidth: int = self._width // self._dimension
        self.__cellHeight: int = self._height // self._dimension

        self.__createButtons()


        self._defineStyleVariables()


    def _defineStyleVariables(self):
        '''
            Defines the variables that get used to style the screen
        '''
        self.__lineThickness = 15

        self.__titleFont = Fonts["verdana_big"]

        self.__lineColor = Colors["black"]
        self.__oddCellColor = Colors["deepBlue"]
        self.__evenCellColor = Colors["petrol"]
        self.__titleColor = Colors["black"]



    def display(self, window: Surface) -> None:
        self.__drawCells(window)

        self.__drawHorizontalLines(window)

        self.__drawVerticalLines(window)

        self.__drawTitle(window)

        self.__startGameButton.display(window)

    
    def __drawCells(self, window: Surface) -> None:
        '''
            Draws the cells of the tic-tac-toe grid in alternate colors
        '''
        for row in range(self._dimension):
            for column in range(self._dimension):
                index: int = row * self._dimension + column + 1
                color: Tuple[int, int, int] = self.__oddCellColor if index % 2 == 1 else self.__evenCellColor
                
                positionX: int = column * self.__cellWidth
                positionY: int = row * self.__cellHeight

                pygame.draw.rect(window, color, (positionX, positionY, self.__cellWidth, self.__cellHeight))



    def __drawHorizontalLines(self, window: Surface) -> None:
        '''
            Draws the horizontal lines of the tic-tac-toe grid
        '''
        for i in range(self._dimension - 1):
            lineHeight: int = (i + 1) * self.__cellHeight
            pygame.draw.line(window, self.__lineColor, (0, lineHeight), (self._width, lineHeight), self.__lineThickness)


    def __drawVerticalLines(self, window: Surface) -> None:
        '''
            Draws the vertical lines of the tic-tac-toe grid
        '''
        for i in range(self._dimension - 1):
            lineWidth: int = (i + 1) * self.__cellWidth
            pygame.draw.line(window, self.__lineColor, (lineWidth, 0), (lineWidth, self._height), self.__lineThickness)


    def __drawTitle(self, window: Surface) -> None:
        '''
            Displays a title called "Tic Tac Toe" in the upper row of the grid of the menu. 
            Each word is center in one of the 3 cells
        '''
        ticSurface: Surface = self.__titleFont.render("Tic", False, self.__titleColor)
        tacSurface: Surface = self.__titleFont.render("Tac", False, self.__titleColor)
        toeSurface: Surface = self.__titleFont.render("Toe", False, self.__titleColor)

        ticRect: Rect = pygame.Rect(0 * self.__cellWidth, 0, self.__cellWidth, self.__cellHeight)
        tacRect: Rect = pygame.Rect(1 * self.__cellWidth, 0, self.__cellWidth, self.__cellHeight)
        toeRect: Rect = pygame.Rect(2 * self.__cellWidth, 0, self.__cellWidth, self.__cellHeight)

        window.blit(ticSurface, self._centerSurfaceInRect(ticSurface, ticRect))
        window.blit(tacSurface, self._centerSurfaceInRect(tacSurface, tacRect))
        window.blit(toeSurface, self._centerSurfaceInRect(toeSurface, toeRect))
    
    
    def __createButtons(self) -> None:
        '''
            Creates the buttons that exist in the screen of the menu
        '''
        # Button that starts the game
        startGameButtonX: int = self._width // 2 - 50
        startGameButtonY: int = self._height // 2 - 30

        self.__startGameButton: Button = Button(startGameButtonX, startGameButtonY, 100, 60, "Start Game", "gameScreen", 10)

        self.__startGameButton.style(Colors["orangeIdle"], Colors["orangeActive"], Colors["deepNavyBlue"], Fonts["verdana_tiny_bold"])

        


    def handleEvents(self, events: List[Event], callBackForNavigation):
        '''
            Handles the events for the menu screen.
        '''
        self.__startGameButton.handleEvents(events, callBackForNavigation)
        