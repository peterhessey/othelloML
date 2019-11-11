import numpy as np  
import networkx as nx
import random
import math
import time
import othelloBoard


# 5 seconds per move
MAX_TIME = 5

class MC_agent:
    def __init__(self, verbose):
        self.verbose = verbose
        self.nodes = {}

    def getNextBoardState(root_board_state, dark_turn):
        start_time = time.time()
        """The MCTS algortihm goes here

        structure:
        while resourcesLeft():
            leaf = traverse(root(boardState?))
            simulation_result = rollout(leaf)
            backpropogate(leaf, simulation_result)
        return best_child(root)
        """
        game_tree = nx.Graph()
        
        #creating and adding root node to graph
        node = Node(othelloBoard.OthelloBoard(root_board_state,
                                                         dark_turn))
        game_tree.add_node(node)

        #while the time for making each move has not been maxed out
        while (time.time() - start_time) > MAX_TIME:
            
        return None

    def traverseNode(self, node):
        return None

    def rollout(node):
        return None
        
class Node:
    def __init__(self, board, dark_turn):
        #board is an OthelloBoard object
        self.board = board
        self.reward = 0
        self.visits = 0
        self.fullyExpanded = False

    def getReward(self):
        return self.reward

    def getVisits(self):
        return self.vists

    def getChildren(self):
        return [othelloBoard.OthelloBoard(child_board_state, not self.board.getDarkTurn()) for child_board stateself.board.getChildren()]