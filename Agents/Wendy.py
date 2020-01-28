import torch
import numpy as np

from monteCarloPlayer import MCAgent, Node
from othelloCNNPlayer import CNNPlayer
import DeepLearning
import Othello as oth

class Wendy(MCAgent, CNNPlayer):

    def __init__(self, verbose, dark_player, time_per_move=1):
        # set up MC 
        super(MCAgent, self).__init__(verbose, dark_player, time_per_move)
        
        # set up CNN
        super(CNNPlayer, self).__init__(verbose, dark_turn)
        
        # generate own move map
        self.move_map = self.generateMoveToIntMap()


    def generateMoveToIntMap(self):
    """Generates a dictionary that maps move coordinates to an integer from 0
    to 59
    
    Returns:
        {(int,int):int} -- [Map from move tuple to representative integer]
    """

    move_map = {}
    move_num = 0
    for i in range(8):
        for j in range(8):
            if not ((i == 3 or i == 4) and (j == 3 or j == 4)):
                move_map[(i,j)] = move_num
                move_num += 1

    return move_map 


    # uses MCAgent getBoardState
    def getNextBoardState(self, board_state):
        MCAgent.getNextBoardState(board_state)


#################NOT FINISHED ######################################
# Need to find a way to convert Node board states into the integer output from
# the CNN

    # will use weighted sum of CNN and MC output to determine best node
    def getBestNode(self, root, board_state):

        # retrieve valid moves and the children associated with those moves
        valid_moves = board.getValidMoves()
        
        move_board_pairs = []
        move_count = 0
        for move in valid_moves:
            move_board_pairs.append((move, root.children[move_count]))
            move_count += 1


        # retrieve move probabilities from CNN
        board = oth.OthelloBoard(board_state, self.dark_player)
        network_input = self.getNetworkInputFromBoard(board_state)

        # check if any valid moves available
        if bool(valid_moves):
            with torch.no_grad():
                # extract the probability of selecting each move, put into list
                move_probabilities = self.cnn(network_input).squeeze().tolist()
        
            # set up tracking parameters        
            best_node_score = float('-inf')
            best_node = root    

            for move, child_node in move_board_pairs:
                monte_carlo_score = float(child_node.reward \
                    / child_node.visits)
                
                # get the probability from the CNN using Wendy's move map
                cnn_score = move_probabilities[self.move_map[move]]

                # simply multiplying them for now MAY CHANGE THIS IN THE FUTURE
                node_score = monte_carlo_score * cnn_score

                print(
                    'Scores ---',
                    'MC-Score:', monte_carlo_score,
                    'CNN-Score:', cnn_score
                )

                if node_score > best_node_score:
                    best_node_score = node_score
                    best_node = child_node

            return best_node.board.board_state

        else:
            return np.array([0])


        
        

            