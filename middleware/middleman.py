from typing import Tuple

from backend.game import Game
from backend.game import PlayerMoveResponse


class Middleman:
    def __init__(self):
        self.__game: Game = Game()

    def play(self, coordinates: Tuple[int, int]) -> str:
        response: PlayerMoveResponse = self.__game.playFromFrontend(coordinates)

        return response.message