from backend.components.state import State
from backend.algorithms.evaluationMethods.threeTwoOneEvaluation import ThreeTwoOneEvaluation
from backend.algorithms.utils import findOpponent

class MiniMax:
    def __init__(self, playerA: str, playerB: str):
        self.players: tuple[str, str] = (playerA, playerB)
        self.childOptions: list[tuple[State, int]] = [] #it will save the direct children States of the State for which 
        #the MiniMax algorithm will be called, and their minimax value

        self.__evaluationMethod: ThreeTwoOneEvaluation = ThreeTwoOneEvaluation(self.players)
        self.__algorithmPlayer: str = " " #the player for which the algorithm was initially called


    def miniMax(self, state, depth: int, player: str) -> State:
        '''
            Reviews the states that can occur from the given {state}, if the {player} makes his move.
            The most beneficial state for the {player} is returned.

            Parameters:
                player (str): The symbol of one tic-tac-toe player
                state (State): A snapshot of the tic-tac-toe game for which we want to determine the next best move 
                    the {player} can make
                depth (int): A number that specifies how deep the algorithm will search the minimax tree
        '''
        self.__algorithmPlayer = player
        minimaxValue: int = self.__execute(state, True, depth, player, True)

        for option in self.childOptions:
            if (option[1] == minimaxValue):
               return option[0]

    
    def __execute(self, state: State, maximizePlayer: bool, depth: int, player: str, firstTime: bool) -> int:  
        '''
            Recursive function that performs the MiniMax algorithm. If the state being reviewed is final, which means 
            some of the three conditions are fulfilled:
            a) a player is winning the game 
            b) the grid is full (game ended)
            c) algorithm reach maximum depth specified

            then the state is evaluated and value is returned.

            If maximizePlayer is true, then the algorithm finds the maximum value of the child-states.
            If maximizePlayer is false, then the algorithm finds the minimum value of the child-states.
            This value is called minimax value for the given state, and is returned when function ends.

            The algorithm saves the child-states of the "prototype" state (the state for which the algorithm run for first time)
            and their minimax value so as to be used to determine the most beneficial next move, when the current state of the
            tic-tac-toe game is the prototype state
        '''   
        if (depth == 0 or state.isVictory() or state.gridIsFull()):
            return self.__evaluationMethod.evaluate(state, self.__algorithmPlayer)
        
        opponent: str = findOpponent(player, self.players)
        childStates: list[State] = state.getChildStates(player)

        if (maximizePlayer):
            value: int = -1000
            childValue: int = 0
            for child in childStates:
                childValue = self.__execute(child, not maximizePlayer, depth - 1, opponent, False)
                value = childValue if childValue > value else value

                if (firstTime):
                    self.childOptions.append((child, childValue))

        else:
            value: int = 1000
            childValue: int = 0
            for child in childStates:
                childValue = self.__execute(child, not maximizePlayer, depth - 1, opponent, False)
                value = childValue if childValue < value else value

                if (firstTime):
                    self.childOptions.append((child, childValue))


        return value



    


    

