from typing import Tuple

from backend.game import Game


class Middleman:
    def __init__(self):
        self.__game: Game = Game()

    def play(self, coordinates: Tuple[int, int]):
        pass