from typing import Dict
import pygame


Colors: Dict[str, tuple[int, int, int]] = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0)
}


Fonts: Dict[str, pygame.font.Font] = {
    "verdana": pygame.font.SysFont('verdana',  70)
}