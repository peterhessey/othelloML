import argparse
import numpy as np
import torch
import othelloBoard as board

MASTER_PATH = 'C:/Users/Peter/Documents/UNIVERSITY/Year_3/Individual_Project/othelloML/Data/'

def extractBoardStates(filename):
    file_path = MASTER_PATH + filename + '.wtb'

    games = []
    with open(file_path, 'rb') as games_file:
        game_data = games_file.read()

        number_of_games = int.from_bytes(game_data[4:8], 'little')
        
        print('Number of games in file:', number_of_games)

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

        
    board_state_triples = getBoardStatesFromMoves(games)
    print('All games succesfully processed!')

    board_data, moves = processTriples(board_state_triples)

    np.save(MASTER_PATH + filename + 'boards', board_data)
    np.save(MASTER_PATH + filename + 'moves', moves)


def getBoardStatesFromMoves(games):

    board_state_triples = []

    start_board_state = np.full((8,8), 'x')
    start_board_state[3,3] = 'w'
    start_board_state[4,4] = 'w'
    start_board_state[3,4] = 'd'
    start_board_state[4,3] = 'd'

    game_counter = 0
    for game in games:
        dark_turn = True
        current_board_state = np.copy(start_board_state)

        for move in game:
            current_board = board.OthelloBoard(current_board_state, dark_turn)
            
            valid_moves = current_board.getValidMoves()

            # checks if a player had to skip a turn
            if move not in valid_moves:
                dark_turn = not dark_turn
                current_board = board.OthelloBoard(current_board_state, dark_turn)       
                valid_moves = current_board.getValidMoves()

            board_state_triples.append([current_board_state, dark_turn, move])

            current_board_state = current_board.makeMove(move, valid_moves[move])

            if len(current_board_state) != 1:
                dark_turn = not dark_turn
                
            else:
                print('Invalid move input :(, move was:', move)
                print('Game:', game)

        game_counter += 1
        if game_counter % 100 == 0:
            print('Processed game', game_counter)

    return board_state_triples


def processTriples(board_state_triples):
    
    move_map = generateMoveToIntMap()

    all_boards_data = []
    moves = []
    for board_state, dark_turn, move in board_state_triples:
        board_data = np.full((2,8,8), 0)

        for i in range(8):
            for j in range(8):
                board_char = board_state[i,j]

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

    return all_boards_data, moves

def generateMoveToIntMap():

    move_map = {}
    move_num = 0
    for i in range(8):
        for j in range(8):
            if not ((i == 3 or i == 4) and (j == 3 or j == 4)):
                move_map[(i,j)] = move_num
                move_num += 1

    return move_map 
def loadTensorData(filename):
    board_data = np.load(MASTER_PATH + filename + 'boards.npy')
    moves = np.load(MASTER_PATH + filename + 'moves.npy')

    boards_tensor = torch.as_tensor(board_data)
    moves_tensor = torch.as_tensor(moves)

    return boards_tensor, moves_tensor


if __name__ == "__main__":
    filename = 'WTH_2018'
    extractBoardStates(filename)
    network_input, moves = loadTensorData(filename)
    print(network_input.shape)
    print(moves.shape)
    