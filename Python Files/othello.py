# Tutorial found on this website: https://ukdevguy.com/tutorial-on-how-to-draw-shapes-in-pygame/

import pygame
import sys
import math


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

class Game:


    def __init__(self):
        self.white_turn = True
        self.board = self.generateBoard()


    def generateBoard(self):
        """Generates a new board array for the game object
        
        Returns:
            new_board -- The generated new board
        """
        new_board = []

        for _ in range(8):
            column = []
            for _ in range(8):
                column.append('x')
            
            new_board.append(column)
        
        new_board = self.createStartPosition(new_board)
        return new_board


    def createStartPosition(self, new_board):
        """Places the starting pieces on the board
        
        Arguments:
            new_board {[[Chr]]} -- The new (empty) board
        
        Returns:
            new_board -- The new board with starting pieces placed
        """
        new_board[3][3] = 'b'
        new_board[4][4] = 'b'
        new_board[3][4] = 'w'
        new_board[4][3] = 'w'
        return new_board


    def run(self):
        """The main function for running the game object
        """
        pygame.init()

        # Create a game window
        game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Othello")
        
        game_running = True
        print("Starting game...")
        
        while game_running:
            self.drawBoard(game_window)

            valid_moves = self.getValidMoves()
            move = (-1,-1)

            while (move not in valid_moves) & game_running:
                move, game_running = self.getMove()
            
            self.makeMove(move)
                                    
        
        pygame.quit()

    def drawBoard(self, game_window):
        """Draws the current game state to the screen
        
        Arguments:
            game_window {pygame.window object (?)} -- The game window on the screen
        """
        game_window.fill((0,157,0))
        for i in range(8):
            for j in range(8):
                rect = pygame.Rect(i*100,j*100,100,100)
                pygame.draw.rect(game_window, (0,0,0), rect, 5)

                piece_val = self.board[i][j]

                if piece_val == 'w':
                    pygame.draw.circle(game_window, (255,255,255), (i*100 + 50, j*100 + 50), 40, 0)
                elif piece_val == 'b':
                    pygame.draw.circle(game_window, (0,0,0), (i*100 + 50, j*100 + 50), 40, 0)

        
        pygame.display.update()

        
    def getValidMoves(self):
        """Returns a list of valid moves the current player can make
        
        Returns:
            [(Integer,Integer)] -- The list of valid moves
        """
        valid_moves = []

        adjacent_squares_dict = self.getAdjacentSquares()
        print(adjacent_squares_dict)                

        
        return valid_moves


    def getAdjacentSquares(self):
        """Gets a list of all squares adjacent to an opponent's piece
        
        Returns:
            [(Integer,Integer)] -- List of adjacent squares
        """

        adjacent_squares_dict = {}

        player_char = self.getCurrentOpponent()
        
        for i in range(8):
            for j in range(8):

                if self.board[i][j] == 'x':
                    for x in range(-1, 1):
                        for y in range(-1, 1):
                            
                            square_to_check = (i+x, j+y)
                            
                            try:
                                if self.board[square_to_check[0]][square_to_check[1]] == player_char:
                                    adjacent_squares_dict[(i,j)] = (x,y)
                            except:
                                pass



        return adjacent_squares_dict


    def getMove(self):
        """Takes a user input of a move
        
        Returns:
            (Integer,Integer), Bool -- The registered move, or whether 
                                       the user has quit the game
        """
        move = (-1,-1)
        game_running = True

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_input = event.pos
                move = self.convertClickToMove(mouse_input)          
        
        return move, game_running


    def convertClickToMove(self, mouse_input):
        """Converts the user input to a board coordinate
        
        Arguments:
            mouse_input {Mouse input event position} -- The coordinates of the click on screen
        
        Returns:
            [(Integer, Integer)] -- The coordinates of the square the user clicked
        """
        move = (math.floor(mouse_input[0]/100), math.floor(mouse_input[1]/100))
        return move


    def makeMove(self, move):
        """Applies the user's move to the game
        
        Arguments:
            move {(Integer,Integer)} -- The coordinates of the new piece
        """
        
        if self.white_turn:
            new_piece_char = 'w'
        else:
            new_piece_char = 'b'
        
        self.board[move[0]][move[1]] = new_piece_char
        
        self.white_turn = not white_turn


    def getCurrentPlayer(self):
        """Returns the character representation of the current player
        
        Returns:
            Chr -- 'w' = white, 'b' = black
        """
        if self.white_turn:
            return 'w'
        else:
            return 'b'
    

    def getCurrentOpponent(self):
        """Returns the character representation of the current opponent
        
        Returns:
            Chr -- 'w' = white, 'b' = black
        """
        if self.white_turn:
            return 'b'
        else:
            return 'w'

    def flipPieces(self, newMove):
        return None


    def isGameOver(self):
        return False


    def getWinner(self):
        return None


if __name__ == "__main__":
    newGame = Game()

    newGame.run()
