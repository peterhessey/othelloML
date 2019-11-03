import numpy as np 
import random as rand 

class random_player:
    def __init__(self, verbose):
        """Initialises random player
        
        Arguments:
            verbose {Bool} -- Determines if random player is verbose
        """
        self.verbose = verbose

        if self.verbose:
            print("Initialised random player!")

    def getMove(self, board, valid_moves):
        """Randomly selects a move from a list of valid moves
        
        Arguments:
            board {numpy.array([[chr]])} -- Array representation of the game board
            valid_moves {[(int,int)]} -- List of all valid moves   
        
        Returns:
            (int, int) -- Move selected
        """
        number_of_moves = len(valid_moves)
        move_selected = rand.randint(1, number_of_moves) - 1
        move = list(valid_moves)[move_selected]

        return move

    def quitGame(self):
        """Quits game for random player
        """
        if self.verbose:
            print("Random player quitting...")