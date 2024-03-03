from typing import List, Tuple
from enum import Enum

import threading
import time
import math

import pygame
from pygame import Surface

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


    def __determineTotalIncrease(self) -> int:
        match self.__direction:
            case Direction.RIGHT:
                return self.__endX - self.__startX

            case Direction.DOWN:
                return self.__endY - self.__startY
            
    
    def getEndX(self) -> int:
        return self.__endX
    
    def getEndY(self) -> int:
        return self.__endY
        

        

class VictoryVisualizer:
    '''
        This class defines the unit responsible for visualizations of victory type
    '''
    def __init__(self, cellWidth: int, cellHeight: int, lineThickness: int, dimension: int):
        # Parameters
        self.__cellWidth: int = cellWidth
        self.__cellHeight: int = cellHeight
        self.__lineThickness: int = lineThickness
        self.__dimension: int = dimension

        # Class defined variables
        self.__ips = 15 # -> Increases Per Second
        self.__visualizationSteps: List[List[VictoryVisualizationLine]] = []
        self.__completedVisualizationSteps: List[List[VictoryVisualizationLine]] =  []
        self.__offset: int = self.__lineThickness // 2


    def visualize(self, type: VictoryVisualizationType, totalDuration: int) -> None:
        '''
            Sets up and begins the visualization.

            Parameters:
                type (VictoryVisualizationType) -> Declares what visualize will visualize. For example VictoryVisualizationType.FirstRow
                    will draw a red border around the first row of the tic-tac-toe grid
        '''
        print("mphka re sthn visualize")
        visualizationLines: List[VictoryVisualizationLine] = []
        startPointX: int = 0
        startPointY: int = 0

        match type:
            case VictoryVisualizationType.FirstRow:
                visualizationLines = self.__visualizeRow(0)
                startPointX = 0
                startPointY = 0

            case VictoryVisualizationType.SecondRow:
                visualizationLines = self.__visualizeRow(1)
                startPointX = 0
                startPointY = self.__cellHeight

        visualizationLines = self.__sortVisualizationLinesBasedOnAbsoluteDistance(visualizationLines, startPointX, startPointY)
        self.__determineVisualizationSteps(visualizationLines)

        thread: threading.Thread = threading.Thread(target = self.__execute, args=(totalDuration,))
        thread.start()

    
    def display(self, window: Surface, lineColor: Tuple[int, int, int]) -> None:
        '''
            Displays the parts of the visualization in the screen.

            Parameters:
                lineColor (Tuple[int, int, int]) -> The color of the lines that will be visualized
        '''
        for step in self.__visualizationSteps:
            for line in step:
                line.display(window, lineColor)


    def __visualizeRow(self, row: int) -> List[VictoryVisualizationLine]:
        '''
            Determines the lines segments that will form the border of the selected {row}. 
        '''
        
        lines: List[VictoryVisualizationLine] = []

        startPointX: int = 0
        startPointY: int = row * self.__cellHeight

        for x in range(self.__dimension):
            upperLine: VictoryVisualizationLine = VictoryVisualizationLine(
                startX = x * self.__cellWidth,
                startY = startPointY + (self.__offset if row == 0 else 0),
                endX = (x + 1) * self.__cellWidth,
                endY = startPointY,
                direction = Direction.RIGHT,
                ips = self.__ips,
                duration = 1,
                lineThickness = self.__lineThickness
            )

            lowerLine: VictoryVisualizationLine = VictoryVisualizationLine(
                startX = x * self.__cellWidth,
                startY = startPointY + self.__cellHeight,
                endX = (x + 1) * self.__cellWidth,
                endY = startPointY + self.__cellHeight,
                direction = Direction.RIGHT,
                ips = self.__ips,
                duration = 1,
                lineThickness = self.__lineThickness
            )

            lines.append(upperLine)
            lines.append(lowerLine)

        
        leftLine: VictoryVisualizationLine = VictoryVisualizationLine(
            startX = startPointX + self.__offset,
            startY = startPointY,
            endX = startPointX,
            endY = startPointY + self.__cellHeight,
            direction = Direction.DOWN,
            ips = self.__ips,
            duration = 1,
            lineThickness = self.__lineThickness
        )

        rightLine: VictoryVisualizationLine = VictoryVisualizationLine(
            startX = self.__dimension * self.__cellWidth - self.__offset,
            startY = startPointY,
            endX = self.__dimension * self.__cellWidth,
            endY = startPointY + self.__cellHeight,
            direction = Direction.DOWN,
            ips = self.__ips,
            duration = 1,
            lineThickness = self.__lineThickness
        )

        lines.append(leftLine)
        lines.append(rightLine)

        return lines


    def __visualizeColumn(self, column: int) -> List[VictoryVisualizationLine]:
        '''
            Determines the lines segments that will form the border of the selected {column}. 
        '''
        pass


    def __visualizePrimaryDiagonal(self) -> List[VictoryVisualizationLine]:
        '''
            Determines the lines segments that will form the border of the primary diagonal.
        '''
        pass


    def __visualizeSecondaryDiagonal(self) -> List[VictoryVisualizationLine]:
        '''
            Determines the lines segments that will form the border of the secondary diagonal.
        '''
        pass

    
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

    def __execute(self, totalDuration: int):
        '''
            The main logic of the visualization. Keeps visualization going forward in every step.
        '''
        stepDuration: int = totalDuration // len(self.__visualizationSteps)
        sleepTime: int = 1 / self.__ips

        print(self.__ips * stepDuration)
        print(self.__ips, stepDuration, totalDuration)

        for step in self.__visualizationSteps:
            for x in range(self.__ips * stepDuration):
                for line in step:
                    line.expand()
                time.sleep(sleepTime)




