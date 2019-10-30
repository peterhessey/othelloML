import numpy as np
import pygame

class Human:

    def __init__(self, verbose):
        self.verbose = verbose
        
        if self.verbose:
            print("Initialising human player...")
            print('\n\n')
            
    def getMove(self, board):
        move = (0,0)
        return move