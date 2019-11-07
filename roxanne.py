import numpy as np
import random as rand

class Roxanne:

    def __init__(self, verbose):
        """Initialises roxanne othello player
        
        Arguments:
            verbose {bool} -- Whether or not roxanne is verbose
        """
        self.verbose = verbose
        self.board_ranks = np.array([[1,5,3,3,3,3,5,1],
                                    [5,5,4,4,4,4,5,5],
                                    [3,4,2,2,2,2,4,2],
                                    [3,4,2,6,6,2,4,3],
                                    [3,4,2,6,6,2,4,3],
                                    [3,4,2,2,2,2,4,3],
                                    [5,5,4,4,4,4,5,5],
                                    [1,5,3,3,3,3,5,1]])

        if self.verbose:
            print('Initialised roxanne!')
            print('Roxanne is using the following rankings:')
            print(self.board_ranks)
            print('\n\n')

    def getMove(self, board, valid_moves):
        """Returns a valid move selected by roxanne
        
        Arguments:
            board {np.array([[Chr]])} -- An array representation of the current game board
            valid_moves {[(int,int)]} -- Array storing all valid moves as a tuple
        
        Returns:
            (int,int) -- Returns the move selected by roxanne
        """
        
        if len(board) != 8:
            print("Roxanne agent can only play on 8x8 Othello boards.")
            move = (-1,-1)
        else:
            potential_moves = {}            
            for move in valid_moves:
                move_rank = self.board_ranks[move[0]][move[1]]
                if move_rank in potential_moves.keys():
                    potential_moves[move_rank].append(move)
                else:
                    potential_moves[move_rank] = [move]
            
            move = self.getBestMove(potential_moves)
        
        return move

    def getBestMove(self, moves):
        """Given a set of valid moves and their rankings, returns the best one
        
        Arguments:
            moves {int:[(int,int)]} -- A dictionary storing each valid move by their ranking
        
        Returns:
            (int,int) -- The move chosen
        """
        move_rank = 1
        move = (-1,-1)

        while move_rank < 8:
            if move_rank in moves.keys():
                #If there a multiple best moves of one rank, select randomly
                number_of_moves = len(moves[move_rank])
                random_move = rand.randint(1, number_of_moves)
                move = moves[move_rank][random_move -1]
                break
            else:
                move_rank += 1
                continue

        return move