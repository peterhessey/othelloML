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
        
    # uses MCAgent getBoardState
    def getNextBoardState(self, board_state):
        pass

    # will use weighted sum of CNN and MC output to determine best node
    def getBestNode(self, root):
        pass