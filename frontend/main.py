from setup import setupFrontend

setupFrontend()

from windowController import WindowController

controller: WindowController = WindowController()

controller.display()