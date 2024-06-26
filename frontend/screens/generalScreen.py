from typing import Tuple, List

from pygame import Surface, Rect
from pygame.event import Event

class GeneralScreen():
    def __init__(self, width: int, height: int):
        self._width: int = width
        self._height: int = height    
        self._dimension: int = 3

    def display(self, window: Surface) -> None:
        pass

    def handleEvents(self, events: List[Event], callBackForNavigation = None):
        '''
            Handles the events of the screen. 

            Parameters: 
                callBackForNavigation: Function that should be called every time a button that switches the current screen, is clicked.
                    Gets as parameter the screen name
        '''
        pass

    def _defineStyleVariables(self):
        '''
            Defines the variables that get used to style the screen
        '''
        pass
    
    def _centerSurfaceInRect(self, surface: Surface, rectangle: Rect) -> Tuple[int, int]:
        '''
            Centers the given {surface} inside the given {rectangle}.

            Returns:
                The coordinates in pixels (x,y) of the top-left corner of the {surface}, after the center 
                of this {surface} becomes equal to the center of the {rectangle}, which means, 
                {surface} is centered inside {rectangle}
        '''

        x: int = rectangle.centerx - surface.get_width() // 2
        y: int = rectangle.centery - surface.get_height() // 2

        return (x, y)
    