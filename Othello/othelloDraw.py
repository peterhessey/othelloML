import pygame
import numpy as np 
import math

class othelloDrawer:

    def __init__(self, board_size, demo_mode):
        """Initalises the board drawing class
        
        Arguments:
            board_size {int} -- The dimension of the board
            demo_mode {bool} -- Determines if the game is being run in demo
            mode or is being play by a human player.
        """
        self.board_size = board_size
        self.demo = demo_mode
        pygame.init()

        self.game_window = pygame.display.set_mode((self.board_size*80,
                                                    self.board_size*80))

        pygame.display.set_caption("Othello")

    def drawBoard(self, board):
            """Draws the Othello game board using pygame
            
            Arguments:
                board {[[char]]} -- Array representing the current board state
            """
            self.game_window.fill((0,157,0))
            for i in range(self.board_size):
                for j in range(self.board_size):
                    rect = pygame.Rect(i*80,j*80,80,80)
                    pygame.draw.rect(self.game_window, (0,0,0), rect, 5)

                    piece_val = board[i][j]

                    if piece_val == 'w':
                        pygame.draw.circle(self.game_window, (255,255,255),
                                            (i * 80 + 40, j * 80 + 40), 30)
                    elif piece_val == 'd':
                        pygame.draw.circle(self.game_window, (0,0,0),
                                            (i * 80 + 40, j * 80 + 40), 30)
                    elif piece_val == 'v':
                        pygame.draw.circle(self.game_window, (255,255,255),
                                            (i * 80 + 40, j * 80 + 40), 5, 0)

                
                pygame.display.update()

            # If in demo mode, pause in order to properly visualise play
            if self.demo:
                pygame.time.delay(50)

    def getUserInput(self):
        """Gets user input, either clicking on the board or exiting the game
        
        Returns:
            (int,int)) -- The coordinates of the input move. (-2,-2) if they
            select to quit.
        """
        move = (-1,-1)
        pause = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    move = (-2,-2)
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_input = event.pos
                    move = self.convertClickToMove(mouse_input) 

            if pause == False:
                break
        return move 

    def convertClickToMove(self, mouse_input):
        """Converts the user input to a board coordinate
            
        Arguments:
            mouse_input {Mouse input event position} -- The coordinates of the click on screen
            
        Returns:
            (Integer, Integer) -- The coordinates of the square the user clicked
        """
        move = (math.floor(mouse_input[0]/80), math.floor(mouse_input[1]/80))
        return move