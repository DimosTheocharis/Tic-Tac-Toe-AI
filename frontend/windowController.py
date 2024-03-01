from typing import List
import pygame
from pygame import Surface
from pygame.time import Clock
from pygame.event import Event

from screens.gameScreen import GameScreen
from styles.generalStyles import Colors

class WindowController:
    '''
        Handles the displaying, refreshing of the window and the screens switching.
    '''
    def __init__(self):
        self.__width = 600
        self.__height = 700
        self.__fps = 30
        self.__running = True
        self.__currentScreen: GameScreen = GameScreen(self.__width, self.__width)
        self.__window: Surface = pygame.display.set_mode((self.__width, self.__height))
        self.__clock: Clock = pygame.time.Clock()


    def display(self):
        '''
            This is  the general function that is responsible for displaying content in window.
        '''
        while (self.__running):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.__running = False

            self.__handleEvents(events)

            self.__window.fill(Colors["white"])

            self.__currentScreen.display(self.__window)

            pygame.display.flip()

            self.__clock.tick(self.__fps)


    def __handleEvents(self, events: List[Event]) -> None:
        self.__currentScreen.handleEvents(events)




