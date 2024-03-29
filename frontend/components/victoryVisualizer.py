from typing import List, Tuple
from enum import Enum

import threading
import time
import math

import pygame
from pygame import Surface

from projectController import ProjectController

class VictoryVisualizationType(Enum):
    FirstRow = 1
    SecondRow = 2
    ThirdRow = 3
    FirstColumn = 4
    SecondColumn = 5
    ThirdColumn = 6
    PrimaryDiagonal = 7
    SecondaryDiagonal = 8


class Direction(Enum):
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    TOP = 4


class VictoryVisualizationLine:
    def __init__(self, startX: int, startY: int, endX: int, endY: int, direction: Direction, ips: int, duration: int, lineThickness: int):
        # Parameters
        self.__startX: int = startX
        self.__startY: int = startY
        self.__endX: int = endX
        self.__endY: int = endY
        self.__direction: Direction = direction
        self.__lineThickness: int = lineThickness

        # Class defined variables
        self.__currentX: int = startX
        self.__currentY: int = startY
        self.__totalIncrease: int = self.__determineTotalIncrease()
        self.__increase = self.__totalIncrease / (ips * duration)


    def display(self, window: Surface, lineColor: Tuple[int, int, int]):
        '''
            Draws the line in the given {window}

            Parameters:
                lineColor (Tuple[int, int, int]) -> The color of the line
        '''
        pygame.draw.line(window, lineColor, (self.__startX, self.__startY), (self.__currentX, self.__currentY), self.__lineThickness)


    def expand(self):
        match self.__direction:
            case Direction.RIGHT:
                self.__currentX += self.__increase

            case Direction.DOWN:
                self.__currentY += self.__increase

            case Direction.TOP:
                self.__currentY += self.__increase


    def __determineTotalIncrease(self) -> int:
        match self.__direction:
            case Direction.RIGHT:
                return self.__endX - self.__startX

            case Direction.DOWN:
                return self.__endY - self.__startY
            
            case Direction.TOP:
                return self.__endY - self.__startY
            
    def completeVisualization(self):
        '''
            In some cases the visualization won't complete 100% due rounding of float numbers. This method
            fixes this problem by completing the visualizaiton manually 
        '''
        match self.__direction:
            case Direction.RIGHT:
                self.__currentX = self.__endX
            
            case Direction.DOWN:
                self.__currentY = self.__endY

            case Direction.TOP:
                self.__currentY = self.__endY
            
    
    def getEndX(self) -> int:
        return self.__endX
    
    def getEndY(self) -> int:
        return self.__endY
        

        

class VictoryVisualizer:
    '''
        This class defines the unit responsible for visualizations of victory type. This visualization type is performed when
        the game is won by a player. It finds the cells that perform tic-tac-toe and progressively draws a border around them. 
        After that, the visualizer paints with a special color these cells in sequence
    '''
    def __init__(self, cellWidth: int, cellHeight: int, lineThickness: int, dimension: int):
        # Parameters
        self.__cellWidth: int = cellWidth
        self.__cellHeight: int = cellHeight
        self.__lineThickness: int = lineThickness
        self.__dimension: int = dimension
        self.__projectController: ProjectController = ProjectController()

        # Class defined variables
        self.__ips = 15 # -> Increases Per Second
        self.__visualizationSteps: List[List[VictoryVisualizationLine]] = []
        self.__victoryRectangles: List[pygame.Rect] = [] # A list with rectangles that will be colored differently than others
        self.__visualizedVictoryRectangles: List[pygame.Rect] = [] # A list of the self.__victoryRectangles that are already colored differently
        self.__offset: int = self.__lineThickness // 2
        self.__victoryVisualizationLineDuration: int = 0.8
        self.activeVisualization: bool = False # Whether or not visualizion is currently running


    def visualize(self, type: VictoryVisualizationType) -> None:
        '''
            Sets up and begins the visualization.

            Parameters:
                type (VictoryVisualizationType) -> Declares what visualize will visualize. For example VictoryVisualizationType.FirstRow
                    will draw a red border around the first row of the tic-tac-toe grid
        '''
        visualizationLines: List[VictoryVisualizationLine] = []
        startPointX: int = 0
        startPointY: int = 0

        self.activeVisualization = True

        match type:
            case VictoryVisualizationType.FirstRow:
                visualizationLines = self.__visualizeRow(0)
                self.__victoryRectangles = self.__createRectanglesForRow(0)
                startPointX = 0
                startPointY = 0

            case VictoryVisualizationType.SecondRow:
                visualizationLines = self.__visualizeRow(1)
                self.__victoryRectangles = self.__createRectanglesForRow(1)
                startPointX = 0
                startPointY = 1 * self.__cellHeight

            case VictoryVisualizationType.ThirdRow:
                visualizationLines = self.__visualizeRow(2)
                self.__victoryRectangles = self.__createRectanglesForRow(2)
                startPointX = 0
                startPointY = 2 * self.__cellHeight

            case VictoryVisualizationType.FirstColumn:
                visualizationLines = self.__visualizeColumn(0)
                self.__victoryRectangles = self.__createRectanglesForColumn(0)
                startPointX = 0
                startPointY = 0

            case VictoryVisualizationType.SecondColumn:
                visualizationLines = self.__visualizeColumn(1)
                self.__victoryRectangles = self.__createRectanglesForColumn(1)
                startPointX = 1 * self.__cellWidth
                startPointY = 0

            case VictoryVisualizationType.ThirdColumn:
                visualizationLines = self.__visualizeColumn(2)
                self.__victoryRectangles = self.__createRectanglesForColumn(2)
                startPointX = 2 * self.__cellWidth
                startPointY = 0

            case VictoryVisualizationType.PrimaryDiagonal:
                visualizationLines = self.__visualizePrimaryDiagonal()
                self.__victoryRectangles = self.__createRectanglesForPrimaryDiagonal()
                startPointX = 0
                startPointY = 0

            case VictoryVisualizationType.SecondaryDiagonal:
                visualizationLines = self.__visualizeSecondaryDiagonal()
                self.__victoryRectangles = self.__createRectanglesForSecondaryDiagonal()
                startPointX = 0
                startPointY = self.__dimension * self.__cellHeight
            

        visualizationLines = self.__sortVisualizationLinesBasedOnAbsoluteDistance(visualizationLines, startPointX, startPointY)
        self.__determineVisualizationSteps(visualizationLines)


        thread: threading.Thread = threading.Thread(target = self.__execute, args=(len(self.__visualizationSteps) * self.__victoryVisualizationLineDuration,))
        thread.start()

    
    def displayLines(self, window: Surface, lineColor: Tuple[int, int, int]) -> None:
        '''
            Displays the parts of the lines visualization in the screen.

            Parameters:
                lineColor (Tuple[int, int, int]) -> The color of the lines that will be visualized
        '''
        for step in self.__visualizationSteps:
            for line in step:
                line.display(window, lineColor)


    def displayCells(self, window: Surface, cellColor: Tuple[int, int, int]):
        '''
            Displays the parts of the cells visualization in the screen.

            Parameters:
                cellColor (Tuple[int, int, int]) -> The color of the cells that will be visualized
        '''
        for rectangle in self.__visualizedVictoryRectangles:
            pygame.draw.rect(window, cellColor, rectangle)


    def __visualizeRow(self, row: int) -> List[VictoryVisualizationLine]:
        '''
            Determines the lines segments that will form the border of the selected {row}. 
        '''
        
        lines: List[VictoryVisualizationLine] = []

        startPointX: int = 0
        startPointY: int = row * self.__cellHeight

        for k in range(self.__dimension):
            upperLine: VictoryVisualizationLine = VictoryVisualizationLine(
                startX = k * self.__cellWidth,
                startY = startPointY + (self.__offset if row == 0 else 0),
                endX = (k + 1) * self.__cellWidth,
                endY = startPointY,
                direction = Direction.RIGHT,
                ips = self.__ips,
                duration = self.__victoryVisualizationLineDuration,
                lineThickness = self.__lineThickness
            )

            lowerLine: VictoryVisualizationLine = VictoryVisualizationLine(
                startX = k * self.__cellWidth,
                startY = startPointY + self.__cellHeight,
                endX = (k + 1) * self.__cellWidth,
                endY = startPointY + self.__cellHeight,
                direction = Direction.RIGHT,
                ips = self.__ips,
                duration = self.__victoryVisualizationLineDuration,
                lineThickness = self.__lineThickness
            )

            lines.append(upperLine)
            lines.append(lowerLine)

        
        leftLine: VictoryVisualizationLine = VictoryVisualizationLine(
            startX = startPointX + self.__offset,
            startY = startPointY,
            endX = startPointX + self.__offset,
            endY = startPointY + self.__cellHeight,
            direction = Direction.DOWN,
            ips = self.__ips,
            duration = self.__victoryVisualizationLineDuration,
            lineThickness = self.__lineThickness
        )

        rightLine: VictoryVisualizationLine = VictoryVisualizationLine(
            startX = self.__dimension * self.__cellWidth - self.__offset,
            startY = startPointY,
            endX = self.__dimension * self.__cellWidth - self.__offset,
            endY = startPointY + self.__cellHeight,
            direction = Direction.DOWN,
            ips = self.__ips,
            duration = self.__victoryVisualizationLineDuration,
            lineThickness = self.__lineThickness
        )

        lines.append(leftLine)
        lines.append(rightLine)

        return lines


    def __visualizeColumn(self, column: int) -> List[VictoryVisualizationLine]:
        '''
            Determines the lines segments that will form the border of the selected {column}. 
        '''

        lines: List[VictoryVisualizationLine] = []

        startPointX: int = column * self.__cellWidth
        startPointY: int = 0

        for k in range(self.__dimension):
            leftLine: VictoryVisualizationLine = VictoryVisualizationLine(
                startX = startPointX + (self.__offset if column == 0 else 0),
                startY = k * self.__cellHeight,
                endX = startPointX,
                endY = (k + 1) * self.__cellHeight,
                direction = Direction.DOWN,
                ips = self.__ips,
                duration = self.__victoryVisualizationLineDuration,
                lineThickness = self.__lineThickness
            )

            rightLine: VictoryVisualizationLine = VictoryVisualizationLine(
                startX = startPointX + self.__cellWidth,
                startY = k * self.__cellHeight,
                endX = startPointX + self.__cellWidth,
                endY = (k + 1) * self.__cellHeight,
                direction = Direction.DOWN,
                ips = self.__ips,
                duration = self.__victoryVisualizationLineDuration,
                lineThickness = self.__lineThickness
            )

            lines.append(leftLine)
            lines.append(rightLine)
        
        
        upperLine: VictoryVisualizationLine = VictoryVisualizationLine(
            startX = startPointX,
            startY = startPointY + self.__offset,
            endX = startPointX + self.__cellWidth,
            endY = startPointY + self.__offset,
            direction = Direction.RIGHT,
            ips = self.__ips,
            duration = self.__victoryVisualizationLineDuration,
            lineThickness = self.__lineThickness
        )

        lowerLine: VictoryVisualizationLine = VictoryVisualizationLine(
            startX = startPointX,
            startY = self.__dimension * self.__cellHeight - self.__offset,
            endX = startPointX + self.__cellWidth,
            endY = self.__dimension * self.__cellHeight - self.__offset,
            direction = Direction.RIGHT,
            ips = self.__ips,
            duration = self.__victoryVisualizationLineDuration,
            lineThickness = self.__lineThickness
        )

        lines.append(upperLine)
        lines.append(lowerLine)

        return lines


    def __visualizePrimaryDiagonal(self) -> List[VictoryVisualizationLine]:
        '''
            Determines the lines segments that will form the border of the primary diagonal.
        '''

        lines: List[VictoryVisualizationLine] = []

        for k in range(self.__dimension):
            upperLine: VictoryVisualizationLine = VictoryVisualizationLine(
                startX = k * self.__cellWidth + (self.__offset if k > 0 and k < self.__dimension else 0),
                startY = k * self.__cellHeight + (self.__offset if k == 0 else 0),
                endX = (k + 1) * self.__cellWidth + (self.__offset if k > 0 and k < self.__dimension else 0),
                endY = k * self.__cellHeight + (self.__offset if k == 0 else 0),
                direction = Direction.RIGHT,
                ips = self.__ips,
                duration = self.__victoryVisualizationLineDuration,
                lineThickness = self.__lineThickness
            )

            lowerLine: VictoryVisualizationLine = VictoryVisualizationLine(
                startX = k * self.__cellWidth - (self.__offset if k > 0 and k < self.__dimension else 0),
                startY = (k + 1) * self.__cellHeight - (self.__offset if k == self.__dimension - 1 else 0),
                endX = (k + 1) * self.__cellWidth - (self.__offset if k > 0 and k < self.__dimension else 0),
                endY = (k + 1) * self.__cellHeight - (self.__offset if k == self.__dimension - 1 else 0),
                direction = Direction.RIGHT,
                ips = self.__ips,
                duration = self.__victoryVisualizationLineDuration,
                lineThickness = self.__lineThickness
            )

            leftLine: VictoryVisualizationLine = VictoryVisualizationLine(
                startX = k * self.__cellWidth + (self.__offset if k == 0 else 0),
                startY = k * self.__cellHeight,
                endX = k * self.__cellWidth + (self.__offset if k == 0 else 0),
                endY = (k + 1) * self.__cellHeight,
                direction = Direction.DOWN,
                ips = self.__ips,
                duration = self.__victoryVisualizationLineDuration,
                lineThickness = self.__lineThickness
            )

            rightLine: VictoryVisualizationLine = VictoryVisualizationLine(
                startX = (k + 1) * self.__cellWidth - (self.__offset if k == self.__dimension - 1 else 0),
                startY = k * self.__cellHeight,
                endX = (k + 1) * self.__cellWidth - (self.__offset if k == self.__dimension - 1 else 0),
                endY = (k + 1) * self.__cellHeight,
                direction = Direction.DOWN,
                ips = self.__ips,
                duration = self.__victoryVisualizationLineDuration,
                lineThickness = self.__lineThickness
            )
                
            lines.append(upperLine)
            lines.append(lowerLine)
            lines.append(leftLine)
            lines.append(rightLine)

        return lines

    def __visualizeSecondaryDiagonal(self) -> List[VictoryVisualizationLine]:
        '''
            Determines the lines segments that will form the border of the secondary diagonal.
        '''
        
        lines: List[VictoryVisualizationLine] = []

        for k in range(self.__dimension):
            m = self.__dimension - k - 1

            upperLine: VictoryVisualizationLine = VictoryVisualizationLine(
                startX = k * self.__cellWidth,
                startY = m * self.__cellHeight + (self.__offset if k == self.__dimension - 1 else 0),
                endX = (k + 1) * self.__cellWidth,
                endY = m * self.__cellHeight + (self.__offset if k == self.__dimension - 1 else 0),
                direction = Direction.RIGHT,
                ips = self.__ips,
                duration = self.__victoryVisualizationLineDuration,
                lineThickness = self.__lineThickness
            )

            lowerLine: VictoryVisualizationLine = VictoryVisualizationLine(
                startX = k * self.__cellWidth,
                startY = (m + 1) * self.__cellHeight - (self.__offset if k == 0 else 0),
                endX = (k + 1) * self.__cellWidth,
                endY = (m + 1) * self.__cellHeight - (self.__offset if k == 0 else 0),
                direction = Direction.RIGHT,
                ips = self.__ips,
                duration = self.__victoryVisualizationLineDuration,
                lineThickness = self.__lineThickness
            )

            leftLine: VictoryVisualizationLine = VictoryVisualizationLine(
                startX = k * self.__cellWidth + (self.__offset if k == 0 else 0),
                startY = (m + 1) * self.__cellHeight - (self.__offset if k > 0 and k < self.__dimension - 1 else 0),
                endX = k * self.__cellWidth + (self.__offset if k == 0 else 0),
                endY = m * self.__cellHeight - (self.__offset if k > 0 and k < self.__dimension - 1 else 0),
                direction = Direction.TOP,
                ips = self.__ips,
                duration = self.__victoryVisualizationLineDuration,
                lineThickness = self.__lineThickness
            )

            rightLine: VictoryVisualizationLine = VictoryVisualizationLine(
                startX = (k + 1) * self.__cellWidth - (self.__offset if k == self.__dimension - 1 else 0), 
                startY = (m + 1) * self.__cellHeight + (self.__offset if k > 0 and k < self.__dimension - 1 else 0),
                endX = (k + 1) * self.__cellWidth - (self.__offset if k == self.__dimension - 1 else 0),
                endY = m * self.__cellHeight + (self.__offset if k > 0 and k < self.__dimension - 1 else 0),
                direction = Direction.TOP,
                ips = self.__ips,
                duration = self.__victoryVisualizationLineDuration,
                lineThickness = self.__lineThickness
            )
                
            lines.append(upperLine)
            lines.append(lowerLine)
            lines.append(leftLine)
            lines.append(rightLine)

        return lines

    
    def __sortVisualizationLinesBasedOnAbsoluteDistance(self, lines: List[VictoryVisualizationLine], startPointX: int, startPointY: int) -> List[VictoryVisualizationLine]:
        '''
            Sorts the given visualization {lines} objects based on the absolute value of the given
            startPoint: (x, y) = ({startPointX}, {startPointY}) and their endPoint with this formula:

            value = sqrt(startPointX - line.endPointX) ** 2 + (startPointY - line.endPointY) ** 2)
        '''
        n: int = len(lines)
        for i in range(n - 1):
            for j in range(0, n - i - 1):

                valueA = math.sqrt(math.pow(startPointX - lines[j].getEndX(), 2) + math.pow(startPointY - lines[j].getEndY(), 2))
                valueB = math.sqrt(math.pow(startPointX - lines[j + 1].getEndX(), 2) + math.pow(startPointY - lines[j + 1].getEndY(), 2))

                if (valueA > valueB):
                    lines[j], lines[j + 1] = lines[j + 1], lines[j]


        return lines


    def __determineVisualizationSteps(self, lines: List[VictoryVisualizationLine]) -> None:
        '''
            Breaks down the set of the given visualization {lines} into smaller sets that will be visualized in seperated 
            consecutive steps. Saves the steps in {self.__visualizationSteps} property
        '''
        for x in range(len(lines) // 2):
            self.__visualizationSteps.append([lines[2 * x], lines[2 * x + 1]])

        if (len(lines) % 2 == 1):
            # Odd number of lines, the line at the middle was not added inside the list
            self.__visualizationSteps.append([lines[x]])


    def __createRectanglesForRow(self, row: int) -> list[pygame.Rect]:
        '''
            Creates and returns a list of pygame rectangles which correspond to the cells of the given {row}
        '''
        if (row < 0 or row >= self.__dimension):
            return []
        
        result: list[pygame.Rect] = []
        for i in range(self.__dimension):
            result.append(pygame.Rect(i * self.__cellWidth, row * self.__cellHeight, self.__cellWidth, self.__cellHeight))

        return result
    
    
    def __createRectanglesForColumn(self, column: int) -> list[pygame.Rect]:
        '''
            Creates and returns a list of pygame rectangles which correspond to the cells of the given {column}
        '''
        if (column < 0 or column >= self.__dimension):
            return []
        
        result: list[pygame.Rect] = []
        for i in range(self.__dimension):
            result.append(pygame.Rect(column * self.__cellWidth, i * self.__cellHeight, self.__cellWidth, self.__cellHeight))

        return result
    
    
    def __createRectanglesForPrimaryDiagonal(self) -> list[pygame.Rect]:
        '''
            Creates and returns a list of pygame rectangles which correspond to the cells of the primary diagonal
        '''
        result: list[pygame.Rect] = []
        for i in range(self.__dimension):
            result.append(pygame.Rect(i * self.__cellWidth, i * self.__cellHeight, self.__cellWidth, self.__cellHeight))

        return result
    
    
    def __createRectanglesForSecondaryDiagonal(self) -> list[pygame.Rect]:
        '''
            Creates and returns a list of pygame rectangles which correspond to the cells of the secondary diagonal
        '''
        result: list[pygame.Rect] = []
        for i in range(self.__dimension):
            result.append(pygame.Rect(i * self.__cellWidth, (self.__dimension - i - 1) * self.__cellHeight, self.__cellWidth, self.__cellHeight))

        return result
    

    def __execute(self, totalDuration: int):
        '''
            The main logic of the visualization. Keeps visualization going forward in every step.
        '''
        stepDuration: int = totalDuration / len(self.__visualizationSteps)
        sleepTime: int = 1 / self.__ips

        for step in self.__visualizationSteps:
            if (self.__projectController._instance.projectIsTerminated): break
            for x in range(math.trunc(self.__ips * stepDuration)):
                if (self.__projectController._instance.projectIsTerminated): break
                for line in step:
                    if (self.__projectController._instance.projectIsTerminated): break
                    line.expand()
                time.sleep(sleepTime)

            # complete uncompleted visualization
            for line in step:
                line.completeVisualization()

        for rectangle in self.__victoryRectangles:
            self.__visualizedVictoryRectangles.append(rectangle)
            time.sleep(0.2)




