'''
Main othello playing module. Allows any 2 agents to play othello (human, 
random, roxanne, monte-carlo etc).
'''


import numpy as np
import roxanne
import humanPlayer as human
import randomPlayer
import monteCarloPlayer as monteCarlo
import othelloDraw
import time

class Game:

    def __init__(self, args):
        """Initialise Othello game object
        
        Arguments:
            args {Namespace} -- Contains user-input arguments
        """
        self.verbose = args.verbose
        self.board_size = args.size
        self.demo_mode = args.demo
        self.dark_turn = True
        self.board = self.generateInitialBoard()
        self.players = self.setUpPlayers(args.players)        

        #checks if demo mode is on, not needed if already a human playing!
        if self.demo_mode and ('h' not in args.players):
            
            print('Setting up pygame for machine players...')
            self.drawer = othelloDraw.othelloDrawer(self.board_size, True)
        else:
            self.demo_mode = False


    def setUpPlayers(self, player_string):
        """Sets up player objects
        
        Arguments:
            player_string {String} -- String storing types of players, i.e
            "hc" for human v computer, "cc" for computer v computer
        
        Returns:
            [Player] -- Array containing the two player objects
        """
        players = []
        for i in range(2):
            if i == 0:
                dark_player = True
            else:
                dark_player = False

            if player_string[i] == 'h':
                new_player = human.Human(self.verbose, dark_player, 
                                         self.board_size)
            elif player_string[i] == 'r':
                new_player = roxanne.Roxanne(self.verbose, dark_player)
            elif player_string[i] == 'R':                
                new_player = randomPlayer.randomPlayer(self.verbose,
                                                       dark_player)
            elif player_string[i] == 'M':
                new_player = monteCarlo.MCAgent(self.verbose, dark_player)

        
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

        board[centre-1][centre-1] = 'd'
        board[centre][centre] = 'd'
        board[centre-1][centre] = 'w'
        board[centre][centre-1] = 'w'

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
