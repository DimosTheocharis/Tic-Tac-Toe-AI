import pygame
from pygame import Surface
from pygame.time import Clock

from screens.gameScreen import GameScreen
from styles.general import Colors

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
        while (self.__running):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.__running = False

            self.__window.fill(Colors["white"])

            self.__currentScreen.display(self.__window, events)

            pygame.display.flip()

            self.__clock.tick(self.__fps)




