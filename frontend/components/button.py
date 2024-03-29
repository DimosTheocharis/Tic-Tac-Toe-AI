from typing import Tuple

import pygame
from pygame import Rect, Surface

class Button:
    '''
        Represents a button which specific styling that performs an action when clicked
    '''
    def __init__(self, x: int, y: int, width: int, height: int, text: str, borderRadius: int = 0):
        # Parameters
        self.__x: int = x
        self.__y: int = y
        self.__width: int = width
        self.__height: int = height
        self.__text: str = text
        self.__borderRadius: int = borderRadius

        # Class defined variables
        self.__rect: Rect = pygame.Rect(x, y, self.__width, self.__height)


    def style(self, backgroundColor: Tuple[int, int, int], foregroundColor: Tuple[int, int, int], font: pygame.font.Font):
        '''
            Declares properties about the styling of the button
        '''
        self.__backgroundColor = backgroundColor
        self.__foregroundColor = foregroundColor
        self.__font = font

        self.__textLabel: Surface = self.__font.render(self.__text, False, self.__foregroundColor)

        x: int = self.__x + self.__width // 2 - self.__textLabel.get_width() // 2
        y: int = self.__y + self.__height // 2 - self.__textLabel.get_height() // 2
        self.__textLabelRect: Rect = pygame.Rect(x, y, self.__textLabel.get_width(), self.__textLabel.get_height())



    def display(self, window: Surface):
        '''
            Responsible for drawing the button in the screen
        '''
        pygame.draw.rect(window, self.__backgroundColor, self.__rect, border_radius = self.__borderRadius)

        window.blit(self.__textLabel, self.__textLabelRect)


