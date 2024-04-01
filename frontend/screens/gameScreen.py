from typing import List, Tuple
import time
import threading

import pygame
from pygame import Rect, Surface
from pygame.event import Event

from frontend.components.button import Button
from frontend.components.screen import Screen
from screens.generalScreen import GeneralScreen
from styles.generalStyles import Colors, Fonts
from middleware.middleman import Middleman
from components.victoryVisualizer import VictoryVisualizer, VictoryVisualizationType

class GameScreen(GeneralScreen):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        self.__cellWidth: int = self._width // self._dimension
        self.__cellHeight: int = self._height // self._dimension
        self.__informerPanelMessage: str = "Your symbol is X. Play wherether you want."

        self.__middleman: Middleman = Middleman() # The interface between frontend and backend
        self.__thread: threading.Thread | None = None

        self._defineStyleVariables()
        self.__createButtons()

        self.__visualizer: VictoryVisualizer = VictoryVisualizer(self.__cellWidth, self.__cellHeight, self.__lineThickness, self._dimension)


    def _defineStyleVariables(self):
        self.__lineThickness = 15

        self.__symbolFont = Fonts["verdana_big"]
        self.__panelMessageFont = Fonts["verdana_small"]

        self.__lineColor = Colors["black"]
        self.__symbolForegroundColor = Colors["black"]
        self.__panelBackgroundColor = Colors["slateGrey"]
        self.__panelForegroundColor = Colors["black"]
        self.__oddCellColor = Colors["deepBlue"]
        self.__evenCellColor = Colors["petrol"]
        self.__windowBackgroundColor = Colors["slateGrey"]

        self.__victoryCellBackgroundColor = Colors["darkRed"]
        self.__victoryCellBorderColor = Colors["darkerRed"]
    

    def display(self, window: Surface) -> None:
        self.__drawGrid(window)
        self.__drawInformerPanel(window)
        self.__backToMenuButton.display(window)


    def __drawGrid(self, window: Surface):
        '''
            This method is responsible for drawing the Tic-Tac-Toe grid
        '''
        window.fill(self.__windowBackgroundColor)

        self.__drawCells(window)

        self.__visualizer.displayCells(window, self.__victoryCellBackgroundColor)

        self.__drawGridBorder(window)

        self.__drawHorizontalLines(window)

        self.__drawVerticalLines(window)

        self.__drawSymbols(window)

        self.__visualizer.displayLines(window, self.__victoryCellBorderColor)
    


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



    def __drawGridBorder(self, window: Surface) -> None:
        '''
            Draws a border around of the tic-tac-toe grid 
        '''
        offset: int = self.__lineThickness // 2

        pygame.draw.line(window, self.__lineColor, (0, 0 + offset), (self._width, 0 + offset), self.__lineThickness)
        pygame.draw.line(window, self.__lineColor, (self._width - offset, 0), (self._width - offset, self._height), self.__lineThickness)
        pygame.draw.line(window, self.__lineColor, (self._width, self._height - offset), (0, self._height - offset), self.__lineThickness)
        pygame.draw.line(window, self.__lineColor, (0 + offset, self._height), (0 + offset, 0), self.__lineThickness)


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


    
    def __drawSymbols(self, window: Surface) -> None:
        '''
            Draws the symbols of the current tic-tac-game in the corresponding positions
        '''
        for row in range(self._dimension):
            for column in range(self._dimension):
                symbol: str = self.__middleman.getCellSymbol(row, column)
                symbolSurface: Surface = self.__symbolFont.render(symbol, False, self.__symbolForegroundColor)

                positionX: int = (column) * self.__cellWidth + (self.__cellWidth // 2 - symbolSurface.get_width() // 2)
                positionY: int = (row) * self.__cellHeight + (self.__cellHeight // 2 - symbolSurface.get_height() // 2)

                window.blit(symbolSurface, (positionX, positionY))

    
    def __drawInformerPanel(self, window: Surface):
        '''
            This method is responsible for drawing a small window under the grid that informs the player about 
            the state of the game.
        '''
        panelRect: Rect = pygame.draw.rect(window, self.__panelBackgroundColor, (70, self._height, self._width - 70, 100))

        messageSurface: Surface = self.__panelMessageFont.render(self.__informerPanelMessage, False, self.__panelForegroundColor)

        coordinatesInPixels: Tuple[int, int] = self._centerSurfaceInRect(messageSurface, panelRect)

        window.blit(messageSurface, (coordinatesInPixels[0], coordinatesInPixels[1]))



    def handleEvents(self, events: List[Event], callBackForNavigation = None):
        '''
            Handles the events for the game screen. Finds the position of the mouse and 
            converts the x,y coordinates from pixels to grid-coordinates.

        '''
        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (not pygame.mouse.get_pressed()[0]): continue
                x, y = pygame.mouse.get_pos()

                row: int = y // self.__cellHeight
                column: int = x // self.__cellWidth

                self.__informerPanelMessage = self.__middleman.humanWillPlay((row, column))

                # Check if it's computer's turn to play, and if game is running
                if (self.__middleman.currentPlayer.name == "COMPUTER" and self.__middleman.gameStatus.name == "RUNNING"):
                    # Check if no other thread is already created. If there is, this means that an request has already been
                    # made for the computer to play
                    if (self.__thread == None):
                        self.__thread = threading.Thread(target=self.__requestComputerMoveWithDelay)
                        self.__thread.start()
        
        self.__backToMenuButton.handleEvents(events, callBackForNavigation)


    def __requestComputerMoveWithDelay(self):
        time.sleep(0.1)
        self.__informerPanelMessage = "Waiting for the computer to play..."
        time.sleep(0.1)

        self.__informerPanelMessage = self.__middleman.computerWillPlay()
        self.__thread = None

        # check if game ended
        if (self.__middleman.gameStatus.name == "ENDED" and not self.__visualizer.activeVisualization):
            self.__handleGameWinning()


    def __handleGameWinning(self):
        '''
            Starts a graphic visualization for the victory of the computer. 
        '''
        if (self.__middleman.checkIfRowWins(0)):
            self.__visualizer.visualize(VictoryVisualizationType.FirstRow)
       
        elif (self.__middleman.checkIfRowWins(1)):
            self.__visualizer.visualize(VictoryVisualizationType.SecondRow)
        
        elif (self.__middleman.checkIfRowWins(2)):
            self.__visualizer.visualize(VictoryVisualizationType.ThirdRow)
        
        elif (self.__middleman.checkIfColumnWins(0)):
            self.__visualizer.visualize(VictoryVisualizationType.FirstColumn)
        
        elif (self.__middleman.checkIfColumnWins(1)):
            self.__visualizer.visualize(VictoryVisualizationType.SecondColumn)
        
        elif (self.__middleman.checkIfColumnWins(2)):
            self.__visualizer.visualize(VictoryVisualizationType.ThirdColumn)

        elif (self.__middleman.checkIfPrimaryDiagonalWins()):
            self.__visualizer.visualize(VictoryVisualizationType.PrimaryDiagonal)
        
        elif (self.__middleman.checkIfSecondaryDiagonalWins()):
            self.__visualizer.visualize(VictoryVisualizationType.SecondaryDiagonal)


    def __createButtons(self) -> None:
        '''
            Creates the buttons that exist in the screen of the game
        '''
        # Button that goes back to the menu
        backButtonX: int = 10
        backButtonY: int = self._height + 50 - 15

        self.__backToMenuButton: Button = Button(backButtonX, backButtonY, 50, 30, "Back", Screen.MenuScreen, 10)

        self.__backToMenuButton.style(Colors["orangeIdle"], Colors["orangeActive"], Colors["deepNavyBlue"], Fonts["verdana_tiny_bold"])