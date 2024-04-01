from typing import Dict

import pygame

Colors: Dict[str, tuple[int, int, int]] = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "deepBlue": (35, 68, 93),
    "petrol": (93, 127, 153),
    "slateGrey": (86, 120, 146),
    "darkerRed": (75, 10, 10),
    "darkRed": (100, 10, 10),
    "orangeIdle": (255, 160, 122),
    "orangeIdle": (255, 149, 77),
    "orangeActive": (255, 127, 80),
    "orangeActive": (255, 127, 80),
    "deepNavyBlue": (51, 51, 102)
}


Fonts: Dict[str, pygame.font.Font] = {
    "verdana_big": pygame.font.SysFont('verdana',  70),
    "verdana_small": pygame.font.SysFont('verdana', 20),
    "verdana_tiny_bold": pygame.font.SysFont('verdana', 14, True)
}