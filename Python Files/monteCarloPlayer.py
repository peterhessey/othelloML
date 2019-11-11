import numpy as np  
import networkx as nx
import random
import math
import time
import othelloBoard


# 5 seconds per move
MAX_TIME = 5

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
            simulation_result = rollout(leaf)
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
        c = 1
         


    def rollout(node):
        return None

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

    def getReward(self):
        return self.reward

    def getVisits(self):
        return self.vists

    def getChildren(self):
        return self.children