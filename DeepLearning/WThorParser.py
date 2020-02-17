import sys
sys.path.insert(1, './Othello')
sys.path.insert(1, './../Othello')

import argparse
import numpy as np
import torch

from othelloBoard import OthelloBoard

MASTER_PATH = './Data/'

def extractBoardStates(filenames):
    """Extracts and saves to an output file the NN data from the WTHOR files
    
    Arguments:
        filename {str} -- Filename of the WTHOR file to parse
    """
    total_num_of_games = 0
    games = []
    for filename in filenames:
        file_path = MASTER_PATH + filename

        with open(file_path, 'rb') as games_file:
            game_data = games_file.read()

            number_of_games = int.from_bytes(game_data[4:8], 'little')
            # number_of_games = 5
            print('Number of games in file:', number_of_games)
            total_num_of_games += number_of_games
            for game_num in range(number_of_games):
                start_byte = 24 + game_num * 68 # 16 bytes for header, 8 bytes for record data
                move_list_bytes = game_data[start_byte:start_byte+60]
                move_list = []

                for byte in move_list_bytes:
                    move_num = int(byte)
                    
                    if move_num > 0:
                        move_row = move_num // 10 - 1
                        move_col = move_num % 10 - 1

                        move_list.append((move_row, move_col))

                games.append(move_list)

                # for testing only
                break
        print('Processed', filename)

    board_state_triples = getBoardStatesFromMoves(games)
    print('All board states generated')

    board_data, moves = processTriples(board_state_triples)
    print('Board data generated, saving...')

    np.save(MASTER_PATH + 'boardsData', board_data)
    np.save(MASTER_PATH + 'movesData', moves)

    print('Saved!')
    print('%d games processed in total' % total_num_of_games)

def getBoardStatesFromMoves(games):
    """Gets the character board states from the lists of moves
    
    Arguments:
        games {[[(int, int)]]} -- A list of games, each game is a list of move
        tuples.
    
    Returns:
        [[[char,char], bool, (int,int)]] -- List of triples, where each triple is 
        the board state, whose turn it is and the move about to be played.
    """
    board_state_triples = []

    # set up start board
    start_board_state = np.full((8,8), 'x')
    start_board_state[3,3] = 'w'
    start_board_state[4,4] = 'w'
    start_board_state[3,4] = 'd'
    start_board_state[4,3] = 'd'

    game_counter = 0
    number_of_games = len(games)
    for game in games:
        dark_turn = True
        current_board_state = np.copy(start_board_state)

        for move in game:
            current_board = OthelloBoard(current_board_state, dark_turn)
            
            valid_moves = current_board.getValidMoves()

            # checks if a player had to skip a turn
            if move not in valid_moves:
                dark_turn = not dark_turn
                current_board = OthelloBoard(current_board_state, dark_turn)       
                valid_moves = current_board.getValidMoves()

            # use symmetric board properties to get all possible states
            for board_state, sym_move in getSymmetricBoardStates(current_board_state, move):
                board_state_triples.append([board_state, dark_turn, sym_move])

            current_board_state = current_board.makeMove(move, valid_moves[move])

            if len(current_board_state) != 1:
                dark_turn = not dark_turn
                
            else:
                print('Invalid move input :(, move was:', move)
                print('Game:', game)

        game_counter += 1

        if game_counter % 250 == 0:
            print('Processed %s/%s games' % (game_counter, number_of_games))

    return board_state_triples

def getSymmetricBoardStates(board_state, move):
    new_board = np.copy(board_state)
    for v in [True, False]:
        for h in [True, False]:
            for r in [True, False]:

                # flip board and move vertically
                if v:
                    new_board = np.flipud(new_board)
                    move = (7 - move[0], move[1])
                # horizontally flip 
                if h:
                    new_board = np.fliplr(new_board)
                    move = (move[0], 7 - move[1])
                # rotate board by 90 degrees
                if r:
                    new_board = np.rot90(new_board)
                    move = (7 - move[1], move[0])

                yield (new_board, move)


def processTriples(board_state_triples):
    """Converts the triple touples from the previous function into binary 
    arrays suitable for inputting into a NN.
    
    Arguments:
        board_state_triples {[[[chr], bool, (int,int)]]} -- Triples
    
    Returns:
        [np.array, np.array] -- The board states and the corresponding moves
    """
    move_map = generateMoveToIntMap()

    all_boards_data = []
    moves = []
    for board_state, dark_turn, move in board_state_triples:
        board_data = np.full((2,8,8), 0)

        for i in range(8):
            for j in range(8):
                board_char = board_state[i,j]

                # convert all board states to black player's perspective
                if dark_turn:
                    if board_char == 'd':
                        board_data[0][i][j] = 1
                    elif board_char == 'w':
                        board_data[1][i][j] = 1
            
                else:
                    if board_char == 'd':
                        board_data[1][i][j] = 1
                    elif board_char == 'w':
                        board_data[0][i][j] = 1
        
        all_boards_data.append(board_data)
        moves.append(move_map[move])

    return np.array(all_boards_data, dtype=np.float32), np.array(moves, dtype=np.int64)

def generateMoveToIntMap():
    """Generates a dictionary that maps move coordinates to an integer from 0
    to 59
    
    Returns:
        [type] -- [description]
    """
    move_map = {}
    move_num = 0
    for i in range(8):
        for j in range(8):
            if not ((i == 3 or i == 4) and (j == 3 or j == 4)):
                move_map[(i,j)] = move_num
                move_num += 1

    return move_map 

def loadTrainingData():

    boards_data = np.load(MASTER_PATH + 'boardsData.npy')
    moves = np.load(MASTER_PATH + 'movesData.npy')

    return boards_data, moves


if __name__ == "__main__":
    filenames = ['WTH_2013.wtb', 'WTH_2014.wtb', 'WTH_2015.wtb', \
        'WTH_2016.wtb', 'WTH_2017.wtb', 'WTH_2018.wtb']
    extractBoardStates(filenames)
    print('Testing data loading...')
    network_input, moves = loadTrainingData()
    print(network_input.shape)
    print(moves.shape)
    