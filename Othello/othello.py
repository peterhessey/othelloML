'''
Main othello playing module. Allows any 2 agents to play othello (human, 
random, roxanne, monte-carlo etc).
'''

import sys

import numpy as np
import time

from othelloDraw import OthelloDrawer
from Agents import Human, Wendy, MCAgent, CNNPlayer, Player, RandomPlayer, Roxanne

class Game:

    def __init__(self, verbose, board_size, demo_mode, player_strings):

        self.verbose = verbose
        self.board_size = board_size
        self.demo_mode = demo_mode
        self.dark_turn = True
        self.board = self.generateInitialBoard()
        self.players = self.setUpPlayers(player_strings)        

        #checks if demo mode is on, not needed if already a human playing!
        if self.demo_mode and ('h' not in args.players):
            
            print('Setting up pygame for machine players...')
            self.drawer = OthelloDrawer(self.board_size, True)
        else:
            self.demo_mode = False


    def setUpPlayers(self, player_strings):

        players = []
        for i in range(2):
            if i == 0:
                dark_player = True
            else:
                dark_player = False

            if player_strings[i] == 'h':
                new_player = Human(self.verbose, dark_player, 
                                         self.board_size)
            elif player_strings[i] == 'W':
                new_player = Wendy(self.verbose, dark_player, 
                                         self.board_size)
            elif player_strings[i] == 'r':
                new_player = Roxanne(self.verbose, dark_player)
            elif player_strings[i] == 'R':                
                new_player = RandomPlayer(self.verbose,
                                                       dark_player)
            elif player_strings[i] == 'M':
                new_player = MCAgent(self.verbose, dark_player)
            elif player_strings[i] == 'M30':
                new_player = MCAgent(self.verbose, dark_player, 30)
            elif player_strings[i] == 'M10':
                new_player = MCAgent(self.verbose, dark_player, 10)
            elif player_strings[i] == 'C':
                new_player = CNNPlayer(self.verbose, dark_player)

        
            players.append(new_player)



        return players
      

    def generateInitialBoard(self):
        """Generates the initial othello board array
        
        Returns:
            np.array([[Chr]]) -- An array that uses characters to represent 
            pieces, 'x' = blank, 'w' = white, 'd' = dark.
        """
        for i in range(self.board_size):
            row = np.array([[]])
            for _ in range(self.board_size):
                row = np.append(row, 'x')

            if i == 0:
                board = np.array([row])
            else:
                board = np.append(board, [row], axis = 0)

        #Set up initial centre pieces
        centre = int(self.board_size / 2)

        board[centre-1][centre-1] = 'w'
        board[centre][centre] = 'w'
        board[centre-1][centre] = 'd'
        board[centre][centre-1] = 'd'

        return board
    

    def run(self):
        
        """Main function for running the game, loops until game ends.
        
        Returns:
            Chr -- Character representation of winning player / draw
        """

        game_running = True

        while game_running:

            if self.demo_mode:
                self.drawer.drawBoard(self.board)                         
                
            if self.dark_turn:
                player_num = 0
                               
            else:
                player_num = 1
                
            game_running =  self.playNextMove(player_num, False)           

        
        winning_player = self.getWinner()

        return winning_player


    def playNextMove(self, player_num, previous_passed):
     #### add documentation here
        new_board = self.players[player_num].getNextBoardState(self.board)
        self.nextTurn()
        if new_board.ndim == 2:
            self.board = new_board            
            return True
        else:            
            if new_board[0] == 0:   
                if previous_passed: 
                    return False
                else:                                      
                    player_num = (player_num + 1) % 2
                    return self.playNextMove(player_num, True)

            else:
                return False


    def nextTurn(self):
        """Simply switches player turns by changing the boolean variable
        """
        self.dark_turn = not self.dark_turn


    def getWinner(self):
        """Determines the winner of the game once it has finished
        
        Returns:
            Chr -- Character representing whether white won, black won, or a 
            draw has occured.
        """
        white_count = 0
        dark_count = 0

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 'w':
                    white_count += 1
                elif self.board[i][j] == 'd':
                    dark_count += 1

        if white_count > dark_count:
            return 'w'
        elif dark_count > white_count:
            return 'd'
        else:
            return 't'
