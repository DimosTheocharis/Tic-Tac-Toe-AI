import pygame
from pygame import Surface
from pygame.time import Clock

from screens.gameScreen import GameScreen

class WindowController:
    '''
        Handles the displaying, refreshing of the window and the screens switching.
    '''

    
    def __init__(self):
        self.__width = 600
        self.__height = 600
        self.__fps = 30
        self.__running = True
        self.__currentScreen: GameScreen = GameScreen(self.__width, self.__height)
        self.__window: Surface = pygame.display.set_mode((self.__width, self.__height))
        self.__clock: Clock = pygame.time.Clock()

    def display(self):
        while (self.__running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False

            self.__window.fill("purple")

            self.__currentScreen.display(self.__window)

            pygame.display.flip()

            self.__clock.tick(self.__fps)




