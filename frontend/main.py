from setup import setupFrontend
import pygame

setupFrontend()

pygame.init()

from windowController import WindowController

controller: WindowController = WindowController()

controller.display()