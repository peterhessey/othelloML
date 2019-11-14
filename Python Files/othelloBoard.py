import numpy as np 

class OthelloBoard:
    
    def __init__(self, board_state, dark_turn):
        """Constructor method for the OthelloBoard class. This class is used to
        represent a single board state. It can be queried to return a list of 
        valid moves available at that board state, or can be used to retrieve 
        the next board state as a result of making one of the valid moves.
        
        Arguments:
            board_state {[chr]} -- The current board state.
            dark_turn {bool} -- Whether or not it's dark's turn in this current
            board position.
        """
        self.board_state = board_state
        self.dark_turn = dark_turn
        self.board_size = len(board_state)


    def getChildren(self):
        """Returns all board states possible by making a valid move at this 
        position.
        
        Returns:
            [[[chr]]] -- An array of 2-D arrays that store character 
            representations of the board.
        """
        children_board_states = np.array([])
        moves = self.getValidMoves()
        for move in moves:
            children_board_states = np.append(children_board_states,
                                              self.makeMove(move, moves[move]))
        
        return children_board_states


    def getValidMoves(self):
        """Returns a list of valid moves the current player can make
        
        Returns:
            {(Integer,Integer) : [(Integer, Integer)]} -- The list of valid
            moves and the directions in which pieces need to be flipped if 
            that move is played.
        """
        valid_moves = {}        
        adjacent_squares_dict = self.getAdjacentSquares()

        for square in adjacent_squares_dict:
            for direction in adjacent_squares_dict[square]:

                if self.validateMove(square, direction):
                    if square in valid_moves:
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

            opponent_char = self.getCurrentOpponentChar()
            
            for i in range(self.board_size):
                for j in range(self.board_size):

                    if self.board_state[i][j] == 'x':
                        for x in range(-1, 2):
                            for y in range(-1, 2):
                                
                                if ((i + x) < self.board_size 
                                    and (i + x) >= 0
                                    and (j + y) < self.board_size 
                                    and (j + y) >= 0):
                                    
                                    square_scanner = self.board_state[i+x][j+y]
                        

                                    if square_scanner == opponent_char:
                                        if (i,j) in adjacent_squares_dict:
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
        player_char  = self.getCurrentPlayerChar()
        opponenet_char = self.getCurrentOpponentChar()
        
        square_scanner = [square[0] + direction[0] * 2, square[1] + direction[1] * 2]
                
        while (square_scanner[0] <= self.board_size - 1 and square_scanner[0] >= 0
             and square_scanner[1] <= self.board_size -1 and square_scanner[1] >= 0
             and move_valid == False):

            try:
                square_char = self.board_state[square_scanner[0]][square_scanner[1]]
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


    def makeMove(self, move, directions):
        """Makes the selected move and returns the new board state
        
        Arguments:
            move {(int, int)} -- The move selected
            directions {[(int, int)]} -- Directions in which pieces need to be
            flipped as a result of the selected move
        
        Returns:
            [[chr]] -- The new board state as a result of the move
        """

        new_board_state = np.copy(self.board_state)
        self.flipPieces(new_board_state, move, directions)

        new_piece_char = self.getCurrentPlayerChar()
        
        new_board_state[move[0]][move[1]] = new_piece_char

        return new_board_state


    def flipPieces(self, new_board_state, move, directions):
        """Function responsible for flipping pieces on the board when a valid
         move is played by the current player.
            
        Arguments:
            new_board_state {[[chr]]} -- The board state to be changed
            move {(int, int)} -- The move selected
            directions {[(int,int)]} -- The directions in which pieces need
            to be flipped as a result of the selected move
        """

        player_char = self.getCurrentPlayerChar()

        for direction in directions:
            line_flipped = False
            square_to_flip = [move[0]+direction[0], move[1]+direction[1]]

                

            while not line_flipped:
                    
                square_char = new_board_state[square_to_flip[0]][square_to_flip[1]]

                if square_char == player_char:
                    line_flipped = True
                    continue

                else:                        
                    new_board_state[square_to_flip[0]][square_to_flip[1]] = player_char
                    square_to_flip[0] += direction[0]
                    square_to_flip[1] += direction[1]


    def getBoardState(self):
        """Returns the board state being represented by the object
        
        Returns:
            [[chr]] -- The array representation of the current game posittion
        """
        return self.board_state


    def boardFull(self):
        boardFull = True
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board_state[i,j] == 'x':
                    boardFull = False
                    return boardFull

        return boardFull

        
    def getCurrentPlayerChar(self):
        """Returns the character representation of the current player
        
        Returns:
            Chr -- 'w' = white, 'd' = black
        """
        if self.dark_turn:
            return 'd'
        else:
            return 'w'
    

    def getCurrentOpponentChar(self):
        """Returns the character representation of the current opponent
        
        Returns:
            Chr -- 'w' = white, 'd' = black
        """
        if self.dark_turn:
            return 'w'
        else:
            return 'd'