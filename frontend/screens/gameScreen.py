from typing import List, Tuple
import time
import threading

import pygame
from pygame import Rect, Surface
from pygame.event import Event

from screens.generalScreen import GeneralScreen
from styles.generalStyles import Colors, Fonts
from middleware.middleman import Middleman
from components.victoryVisualizer import VictoryVisualizer, VictoryVisualizationType

class GameScreen(GeneralScreen):
    def __init__(self, width: int, height: int):
        self.__width: int = width
        self.__height: int = height    
        self.__dimension: int = 3
        self.__cellWidth: int = self.__width // self.__dimension
        self.__cellHeight: int = self.__height // self.__dimension
        self.__informerPanelMessage: str = "Your symbol is X. Play wherether you want."

        self.__middleman: Middleman = Middleman() # The interface between frontend and backend
        self.__thread: threading.Thread | None = None

        self.__defineStyleVariables()

        self.__visualizer: VictoryVisualizer = VictoryVisualizer(self.__cellWidth, self.__cellHeight, self.__lineThickness, self.__dimension)

    def __defineStyleVariables(self):
        self.__lineThickness = 15

        self.__symbolFont = Fonts["verdana_big"]
        self.__panelMessageFont = Fonts["verdana_small"]

        self.__lineColor = Colors["black"]
        self.__symbolForegroundColor = Colors["black"]
        self.__panelBackgroundColor = Colors["slateGrey"]
        self.__panelForegroundColor = Colors["black"]
        self.__oddCellColor = Colors["deepBlue"]
        self.__evenCellColor = Colors["petrol"]

        self.__victoryCellBackgroundColor = Colors["pink"]
        self.__victoryCellBorderColor = Colors["darkPurple"]
    

    def display(self, window: Surface) -> None:
        self.__drawGrid(window)
        self.__drawInformerPanel(window)



    def __drawGrid(self, window: Surface):
        '''
            This method is responsible for drawing the Tic-Tac-Toe grid
        '''
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
        for row in range(self.__dimension):
            for column in range(self.__dimension):
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
        panelRect: Rect = pygame.draw.rect(window, self.__panelBackgroundColor, (0, self.__height, self.__width, 100))

        messageSurface: Surface = self.__panelMessageFont.render(self.__informerPanelMessage, False, self.__panelForegroundColor)

        coordinatesInPixels: Tuple[int, int] = self._centerSurfaceInRect(messageSurface, panelRect)

        window.blit(messageSurface, (coordinatesInPixels[0], coordinatesInPixels[1]))



    def handleEvents(self, events: List[Event]):
        '''
            Handles the events for the game screen. Finds the position of the mouse and 
            converts the x,y coordinates from pixels to grid-coordinates.

        '''
        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN):
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


                if (self.__middleman.gameStatus.name == "ENDED"):
                    self.__handleGameWinning()


    def __requestComputerMoveWithDelay(self):
        time.sleep(0.1)
        self.__informerPanelMessage = "Waiting for the computer to play..."
        time.sleep(0.1)

        self.__informerPanelMessage = self.__middleman.computerWillPlay()
        self.__thread = None


    def __handleGameWinning(self):
        if (self.__middleman.checkIfRowWins(0)):
            self.__visualizer.visualize(VictoryVisualizationType.FirstRow, 4)
       
        elif (self.__middleman.checkIfRowWins(1)):
            self.__visualizer.visualize(VictoryVisualizationType.SecondRow, 4)
        
        elif (self.__middleman.checkIfRowWins(2)):
            self.__visualizer.visualize(VictoryVisualizationType.ThirdRow, 4)
        
        elif (self.__middleman.checkIfColumnWins(0)):
            self.__visualizer.visualize(VictoryVisualizationType.FirstColumn, 4)
        
        elif (self.__middleman.checkIfColumnWins(1)):
            self.__visualizer.visualize(VictoryVisualizationType.SecondColumn, 4)
        
        elif (self.__middleman.checkIfColumnWins(2)):
            self.__visualizer.visualize(VictoryVisualizationType.ThirdColumn, 4)

        elif (self.__middleman.checkIfPrimaryDiagonalWins()):
            self.__visualizer.visualize(VictoryVisualizationType.PrimaryDiagonal, 6)
        
        elif (self.__middleman.checkIfSecondaryDiagonalWins()):
            self.__visualizer.visualize(VictoryVisualizationType.SecondaryDiagonal, 6)