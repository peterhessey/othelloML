# Tutorial found on this website: https://ukdevguy.com/tutorial-on-how-to-draw-shapes-in-pygame/

import pygame
import sys
import math
import argparse


class Game:

    def __init__(self, verbose, board_size):
        self.verbose = verbose
        self.white_turn = False
        self.board_size = board_size
        self.board = self.generateBoard()


    def generateBoard(self):
        """Generates a new board array for the game object
        
        Returns:
            new_board -- The generated new board
        """
        new_board = []

        for _ in range(self.board_size):
            column = []
            for _ in range(self.board_size):
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

        centre = int(self.board_size / 2)

        new_board[centre-1][centre-1] = 'b'
        new_board[centre][centre] = 'b'
        new_board[centre-1][centre] = 'w'
        new_board[centre][centre-1] = 'w'
        return new_board


    def run(self):
        """The main function for running the game object
        """
        pygame.init()

        # Create a game window
        game_window = pygame.display.set_mode((self.board_size*80,
                                                self.board_size*80))
        pygame.display.set_caption("Othello - Black's Turn")
        
        game_running = True
        print("Starting game...")
        
        while game_running:   
            
            valid_moves = self.getValidMoves()

            if len(valid_moves) == 0:
                '''if there are no valid moves for one player,
                 check if there are any for the other player'''

                self.nextTurn()
                valid_moves = self.getValidMoves()

                if len(valid_moves) == 0:
                    game_running = False
                    continue

            if self.verbose:
                print("Valid moves:" + str(valid_moves))
            
            self.markValidMoves(valid_moves.keys())
            self.drawBoard(game_window)
            self.unmarkValidMoves()

                        
            move = (-1,-1)

            while (move not in valid_moves.keys()) and game_running:
                move, game_running = self.getMove()
            
            self.flipPieces(move, valid_moves[move])
            self.makeMove(move)
            self.nextTurn()

        winning_player = self.getWinner()

        if winning_player == 'w':
            print("White wins!")
        elif winning_player == 'b':
            print("Black wins!")
        else:
            print("Draw")                          
        
        pygame.quit()


    def drawBoard(self, game_window):
        """Draws the current game state to the screen:
            - Fills screen with dark green (0,157,0)
            - Draws the board squares
            - Draws the pieces
            - Draws the markers for possible moves
        
        Arguments:
            game_window {pygame.window object (?)} -- The game window on the screen
        """
        game_window.fill((0,157,0))
        for i in range(self.board_size):
            for j in range(self.board_size):
                rect = pygame.Rect(i*80,j*80,80,80)
                pygame.draw.rect(game_window, (0,0,0), rect, 5)

                piece_val = self.board[i][j]

                if piece_val == 'w':
                    pygame.draw.circle(game_window, (255,255,255), (i * 80 + 40, j * 80 + 40), 30)
                elif piece_val == 'b':
                    pygame.draw.circle(game_window, (0,0,0), (i * 80 + 40, j * 80 + 40), 30)
                elif piece_val == 'v':
                    pygame.draw.circle(game_window, (255,255,255), (i * 80 + 40, j * 80 + 40), 5, 0)

        
        pygame.display.update()

        
    def getValidMoves(self):
        """Returns a list of valid moves the current player can make
        
        Returns:
            {(Integer,Integer) : [(Integer, Integer)]} -- The list of valid
            moves and the directions in which pieces need to be flipped if 
            that move is played.
        """
        valid_moves = {}        
        adjacent_squares_dict = self.getAdjacentSquares()

        if self.verbose:
            print("Adjacent squares: " + str(adjacent_squares_dict))
        
        for square in adjacent_squares_dict.keys():
            for direction in adjacent_squares_dict[square]:

                if self.validateMove(square, direction):
                    if square in valid_moves.keys():
                        valid_moves[square].append(direction)
                    else:
                        valid_moves[square] = [direction]             
        
        
        return valid_moves
    

    def validateMove(self, square, direction):
        """For a given square and direction tuple, returns a boolean value
        representing whether that move is a valid move or not.
        
        Arguments:
            square {(Integer, Integer)} -- The square on which the move would
            be played
            direction {(Integer Integer)} -- A 2D normalised vector
            representing the direction in which the move would connect with
            a piece of the same colour.
        
        Returns:
            Bool -- True if move is valid, false otherwise
        """
        move_valid = False
        player_char  = self.getCurrentPlayer()
        opponenet_char = self.getCurrentOpponent()
        
        square_scanner = [square[0] + direction[0] * 2, square[1] + direction[1] * 2]
                
        while (square_scanner[0] <= self.board_size - 1 and square_scanner[0] >= 0
             and square_scanner[1] <= self.board_size -1 and square_scanner[1] >= 0
             and move_valid == False):

            try:
                square_char = self.board[square_scanner[0]][square_scanner[1]]
            except:
                print("Error with " + str(square_scanner))    

            if square_char == player_char:
                move_valid = True
                break
            elif square_char == opponenet_char:
                square_scanner[0] += direction[0]
                square_scanner[1] += direction[1]
            else:
                break

        return move_valid


    def getAdjacentSquares(self):
        """Returns a dictionary of all adjacent squares and the directions in 
        which the adjacent pieces lie
        
        Returns:
            {(Integer, Integer):[(Integer, Integer)]} -- Dictionary that
            represents the adjacent squares and their relative directions
        """
        
        adjacent_squares_dict = {}

        opponent_char = self.getCurrentOpponent()
        
        for i in range(self.board_size):
            for j in range(self.board_size):

                if self.board[i][j] == 'x':
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            
                            if ((i + x) < self.board_size 
                                and (i + x) >= 0
                                and (j + y) < self.board_size 
                                and (j + y) >= 0):
                                
                                square_scanner = self.board[i+x][j+y]
                    

                                if square_scanner == opponent_char:
                                    if (i,j) in adjacent_squares_dict.keys():
                                        adjacent_squares_dict[(i,j)].append((x,y))
                                    else:
                                        adjacent_squares_dict[(i,j)] = [(x,y)]


        return adjacent_squares_dict

    
    def markValidMoves(self, valid_move_squares):
        """Marks squares that are valid moves with a 'v' character
        
        Arguments:
            valid_moves_squares [(Integer, Integer)] -- List containing tuples representing the valid moves
        
        Returns:
            None
        """
        for move in valid_move_squares:
            self.board[move[0]][move[1]] = 'v'


    def unmarkValidMoves(self):
        """Simply replaces all the valid moves that weren't used with the character 'x'
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 'v':
                    self.board[i][j] = 'x'


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
        move = (math.floor(mouse_input[0]/80), math.floor(mouse_input[1]/80))
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



    def flipPieces(self, move, directions):
        """Function responsible for flipping pieces on the board when a valid
        move is played by the current player.
        
        Arguments:
            move {(Integer, Integer)} -- The move that's been played
            directions {[(Integer, Integer)]} -- The directions in which pieces
            need to flipped.
        """

        player_char = self.getCurrentPlayer()

        for direction in directions:
            line_flipped = False
            square_to_flip = [move[0]+direction[0], move[1]+direction[1]]

            if self.verbose:
                print("Flipping pieces on square %s in direciton %s" % (move, direction))

            while not line_flipped:
                if self.verbose:
                    print("Flipping %s" % (square_to_flip))

                square_char = self.board[square_to_flip[0]][square_to_flip[1]]

                if square_char == player_char:
                    line_flipped = True
                    continue

                else:                        
                    self.board[square_to_flip[0]][square_to_flip[1]] = player_char
                    square_to_flip[0] += direction[0]
                    square_to_flip[1] += direction[1]                


    def getBoard(self):
        """Returns a copy of the board state
        
        Returns:
            [[Chr]] -- The board state
        """
        return self.board

    def nextTurn(self):
        """Changes the turn and displays the correct caption
        """
        self.white_turn = not self.white_turn

        if self.white_turn:
            pygame.display.set_caption("Othello - White's Turn")
        else:
            pygame.display.set_caption("Othello - Black's Turn")


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


    def getWinner(self):
        """Determines the winner of the game once it has finished
        
        Returns:
            Chr -- Character representing whether white won, black won, or a 
            draw has occured.
        """
        white_count = 0
        black_count = 0

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 'w':
                    white_count += 1
                elif self.board[i][j] == 'b':
                    black_count += 1

        if white_count > black_count:
            return 'w'
        elif black_count > white_count:
            return 'b'
        else:
            return 'd'


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run an othello game!')
    parser.add_argument('-v', dest='verbose', action='store_const',
                        const=True, default=False, help='Make the program \
                        verbose.')
    parser.add_argument('-s', dest='size', action='store',
                        nargs=1, default=['8'],
                        help = 'The size of the board, even and >= 4')


    args = parser.parse_args()
    print(args)
    if int(args.size[0]) % 2 == 0 and int(args.size[0]) >= 4:

        newGame = Game(args.verbose, int(args.size[0]))

        newGame.run()

    else:
        print("Invalid board size, must be an even number >= 4.")