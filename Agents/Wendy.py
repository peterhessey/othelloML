import torch
import numpy as np

from monteCarloPlayer import MCAgent, Node
from othelloCNNPlayer import CNNPlayer
import DeepLearning
import Othello

class Wendy(MCAgent, CNNPlayer):

    def __init__(self, verbose, dark_player, time_per_move=1):
        # set up MC 
        super(MCAgent, self).__init__(verbose, dark_player, time_per_move)
        
        # set up CNN
        super(CNNPlayer, self).__init__(verbose, dark_turn)
        
    # need to think about this one, check if can use MC function and merge
    # CNN with getBestNode or got to write entire function from scrath
    def getNextBoardState(self, board_state):
        pass