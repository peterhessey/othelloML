import numpy as np
import roxanne
import human_player as human

class Game:

    def __init__(self, args):
        self.verbose = args.verbose
        self.board_size = args.size
        self.dark_turn = True
        self.dark_player, self.white_player = self.setUpPlayers(args.players)
        self.board = self.generateBoard()


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
            if player_string[i] == 'h':
                new_player = human.Human(self.verbose, self.board_size)
            elif player_string[i] == 'c':
                new_player = roxanne.Roxanne(self.verbose)
        
            players.append(new_player)
        if players[0] == players[1]:
            print("These are the same objcet")
        else:
            print("These are a different object")
        return players[0], players[1]
                

    def generateBoard(self):
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

        if self.verbose:
            print("Initial board array:")
            print(board)
            
        return board
    

    def run(self):

        game_running = True

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
                print("Valid moves are: ")
                print(valid_moves)

            '''
            Valid moves are marked in order to be able to draw them
            onto the board for human players. Maybe move this on the
            human players object?
            '''
            self.markValidMoves(valid_moves.keys())

            move = (-1,-1)

            while (move not in valid_moves.keys()) and game_running:
                
                if self.dark_turn:
                    move, game_running = self.dark_player.getMove(self.board, self.dark_turn)
                    if self.verbose:
                        print("Dark player picked move: %s" % str(move))
                else:
                    move, game_running = self.white_player.getMove(self.board, self.dark_turn)
                    if self.verbose:
                        print("White player picked move: %s" % str(move))

            self.unmarkValidMoves()
            self.makeMove(move, valid_moves[move])
            self.nextTurn()
        
        winning_player = self.getWinner()

        self.white_player.quitGame()
        self.dark_player.quitGame()

        return winning_player


    def getValidMoves(self):
        """Returns a list of valid moves the current player can make
        
        Returns:
            {(Integer,Integer) : [(Integer, Integer)]} -- The list of valid
            moves and the directions in which pieces need to be flipped if 
            that move is played.
        """
        valid_moves = {}        
        adjacent_squares_dict = self.getAdjacentSquares()

        for square in adjacent_squares_dict.keys():
            for direction in adjacent_squares_dict[square]:

                if self.validateMove(square, direction):
                    if square in valid_moves.keys():
                        valid_moves[square].append(direction)
                    else:
                        valid_moves[square] = [direction]             
        
        
        return valid_moves
    

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


    def nextTurn(self):
        """Changes the turn and displays the correct caption
        """
        self.dark_turn = not self.dark_turn


    def makeMove(self, move, directions):
        """Applies the user's move to the game
        
        Arguments:
            move {(Integer,Integer)} -- The coordinates of the new piece
        """
        self.flipPieces(move, directions)

        if self.dark_turn:
            new_piece_char = 'd'
        else:
            new_piece_char = 'w'
        
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
                    
                    square_char = self.board[square_to_flip[0]][square_to_flip[1]]

                    if square_char == player_char:
                        line_flipped = True
                        continue

                    else:                        
                        self.board[square_to_flip[0]][square_to_flip[1]] = player_char
                        square_to_flip[0] += direction[0]
                        square_to_flip[1] += direction[1]                


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


    def getCurrentPlayer(self):
        """Returns the character representation of the current player
        
        Returns:
            Chr -- 'w' = white, 'd' = black
        """
        if self.dark_turn:
            return 'd'
        else:
            return 'w'
    

    def getCurrentOpponent(self):
        """Returns the character representation of the current opponent
        
        Returns:
            Chr -- 'w' = white, 'd' = black
        """
        if self.dark_turn:
            return 'w'
        else:
            return 'd'


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