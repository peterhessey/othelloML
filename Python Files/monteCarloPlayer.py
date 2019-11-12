import numpy as np  
import networkx as nx
import random
import math
import time
import othelloBoard
import roxanne

# 5 seconds per move
MAX_TIME = 10
C_VAL = 1

class MCAgent:
    def __init__(self, verbose):
        self.verbose = verbose
        self.game_tree = nx.DiGraph()

    def getNextBoardState(self, root_board_state, dark_turn):
        start_time = time.time()
        
        
        #game tree set up
        self.game_tree = nx.DiGraph()    
        root = Node(othelloBoard.OthelloBoard(root_board_state, dark_turn))
        self.game_tree.add_node(root)


        #while the time for making each move has not been maxed out
        while (time.time() - start_time) > MAX_TIME:
            leaf = traverse(root)
            simulation_result = rollout(leaf)#####################
        return None

    def traverse(self, node):
        while node.fullyExpanded:
            node = bestChildUCT(node)
        
        if node.children == []:
            node.generateChildren()

        for i in range(len(node.children)):
            if node.children[i].visits == 0:
                self.game_tree.add_node(node.children[i])
                self.game_tree.add_edge(node, node.children[i])
                
                if i == len(node.children) - 1:
                    node.fullyExpanded = True

                return node.children[i]
        

    def bestChildUCT(self, node):
        
        max_UCT_value = float('-inf')
        max_node = None

        for child in node.children:
            child_UCT = child.getUCT(node.visits)
            if child_UCT > max_UCT_value:
                max_node = child
                max_UCT_value = child_UCT

        return max_node


    def rollout(self, node):
        game_not_over = True
        rollout_policy = roxanne.Roxanne()
        while game_not_over:
###############################################


class Node:
    def __init__(self, board):
        #board is an OthelloBoard object
        self.board = board
        self.reward = 0
        self.visits = 0
        self.fullyExpanded = False
        self.children = []


    def generateChildren(self):
        for child_board_state in self.board.getChildren():
            child_node_board = othelloBoard.OthelloBoard(child_board_state,
                                                not self.board.getDarkTurn())
            self.children.append(Node(child_node_board))

    def getUCT(self, parent_node_visits):
        return (self.reward / self.visits) + C_VAL * \
                math.sqrt(math.log(parent_node_visits)/self.visits)