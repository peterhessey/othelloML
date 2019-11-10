import numpy as np
import random as rand
import othelloBoard
from Player import Player

class Roxanne(Player):

    def __init__(self, verbose, dark_player):

        self.verbose = verbose
        self.dark_player = dark_player
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

    def getNextBoardState(self, board_state):
        
        
        if len(board_state) != 8:
            print("Roxanne agent can only play on 8x8 Othello boards.")
            board_to_return = np.array([0])
        else:
            board = othelloBoard.OthelloBoard(board_state, self.dark_player)
            valid_moves = board.getValidMoves()

            if bool(valid_moves):
                potential_moves = {}            
                for move in valid_moves:
                    move_rank = self.board_ranks[move[0]][move[1]]
                    if move_rank in potential_moves.keys():
                        potential_moves[move_rank].append(move)
                    else:
                        potential_moves[move_rank] = [move]
                
                move = self.getBestMove(potential_moves)

                board_to_return = board.makeMove(move, valid_moves[move])
            else:
                board_to_return = np.array([0])

        return board_to_return

    def getBestMove(self, moves):
        """Given a set of valid moves and their rankings, returns the best one
        
        Arguments:
            moves {int:[(int,int)]} -- A dictionary storing each valid move by their ranking
        
        Returns:
            (int,int) -- The move chosen
        """
        move_rank = 1
        move = (-1,-1)

        while move_rank < 6:
            if move_rank in moves:
                #If there a multiple best moves of one rank, select randomly
                number_of_moves = len(moves[move_rank])
                random_move = rand.randint(1, number_of_moves)
                move = moves[move_rank][random_move -1]
                break
            else:
                move_rank += 1
                continue

        return move