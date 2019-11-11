import numpy as np  
import random
import math

class MC_agent:
    def __init__(self, verbose):
        self.verbose = verbose

    def getNextBoardState(board_state, dark_turn):
        """The MCTS algortihm goes here

        structure:
        while resourcesLeft():
            leaf = traverse(root(boardState?))
            simulation_result = rollout(leaf)
            backpropogate(leaf, simulation_result)
        move = (-1,-1)
        return (move)

    