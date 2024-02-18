def findOpponent(player: str, players: tuple[str, str]) -> str:
        '''
            Finds the symbol that the opponent of the given player uses
        '''
        return players[0] if player == players[1] else players[1]