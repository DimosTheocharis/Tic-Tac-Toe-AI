from typing import List
from enum import Enum

import threading
import time

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
    def __init__(self, startX: int, startY: int, endX: int, endY: int, direction: Direction, ips: int, duration: int):
        # Parameters
        self.__startX: int = startX
        self.__startY: int = startY
        self.__endX: int = endX
        self.__enxY: int = endY
        self.__direction: Direction = direction

        # Class defined variables
        self.__currentX: int = 0
        self.__currentY: int = 0
        self.__sleepTime: int = 1 / ips
        self.__totalIncrease: int = 0
        self.__increase = self.__totalIncrease / (ips * duration)

        

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
        self.__ips = 10 # -> Increases Per Second
        self.__visualizationSteps: List[List[VictoryVisualizationLine]] = []
        self.__completedVisualizationSteps: List[List[VictoryVisualizationLine]] =  []


    def visualize(self, type: VictoryVisualizationType, totalDuration: int) -> None:
        pass

    
    def display(self) -> None:
        pass


    def __visualizeRow(self, row: int) -> List[VictoryVisualizationLine]:
        '''
            Determines the lines segments that will form the border of the selected {row}. 
        '''

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
        pass



