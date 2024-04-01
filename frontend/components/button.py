from typing import Tuple, List

import pygame
from pygame import Rect, Surface
from pygame.event import Event

class Button:
    '''
        Represents a button which specific styling that performs an action when clicked
    '''
    def __init__(self, x: int, y: int, width: int, height: int, text: str, screenName: str, borderRadius: int = 0):
        # Parameters
        self.__x: int = x
        self.__y: int = y
        self.__width: int = width
        self.__height: int = height
        self.__text: str = text
        self.__screenName: str = screenName
        self.__borderRadius: int = borderRadius

        # Class defined variables
        self.__rect: Rect = pygame.Rect(x, y, self.__width, self.__height)


    def style(self, 
              backgroundColor: Tuple[int, int, int], 
              hoverColor: Tuple[int, int, int],
              foregroundColor: Tuple[int, int, int], 
              font: pygame.font.Font, 
            ):
        '''
            Declares properties about the styling of the button
        '''
        self.__backgroundColor = backgroundColor
        self.__hoverColor = hoverColor
        self.__foregroundColor = foregroundColor
        self.__font = font

        self.__currentBackgroundColor = self.__backgroundColor

        self.__textLabel: Surface = self.__font.render(self.__text, False, self.__foregroundColor)

        x: int = self.__x + self.__width // 2 - self.__textLabel.get_width() // 2
        y: int = self.__y + self.__height // 2 - self.__textLabel.get_height() // 2
        self.__textLabelRect: Rect = pygame.Rect(x, y, self.__textLabel.get_width(), self.__textLabel.get_height())



    def display(self, window: Surface):
        '''
            Responsible for drawing the button in the screen
        '''
        pygame.draw.rect(window, self.__currentBackgroundColor, self.__rect, border_radius = self.__borderRadius)

        window.blit(self.__textLabel, self.__textLabelRect)

    
    def handleEvents(self, events: List[Event], callBackForNavigation):
        '''
            Detects button hover event and button click event
        '''
        x, y = pygame.mouse.get_pos()

        # Check if user hovers over button
        if (self.__rect.collidepoint(x, y)):
            self.__currentBackgroundColor = self.__hoverColor
        else:
            self.__currentBackgroundColor = self.__backgroundColor
            return

        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN):
                callBackForNavigation(self.__screenName)

