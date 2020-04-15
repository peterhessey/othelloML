# Program for playing agents against one another efficiently using parallel
# programming.

import time
import multiprocessing as mp
import matplotlib.pyplot as plt
import argparse
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

from Othello import Game

def runSerialGames():

    results = [0,0,0] #black, white, draws
    for i in range(NUM_OF_GAMES):
        
        game = Game(False, 8, False, [BLACK_PLAYER, WHITE_PLAYER])
        winning_player = game.run()
        # print('Serial completed game %d/%d' %(i+1, NUM_OF_GAMES))

        if winning_player == 'b':
            results[0] += 1
        elif winning_player == 'w':
            results[1] += 1
        else:
            results[2] += 1

    return results

def runParallelGames(num_of_games, black_player, white_player):
    queue = mp.Queue()
    processes = [mp.Process(target=parallelGame, args=(queue, i+1, black_player, white_player,)) for i in range(num_of_games)]

    for p in processes:
        p.start()
    
    for p in processes:
        p.join()

    results = [0,0,0] # black, white, draw
    for _ in range(num_of_games):
        result = queue.get()
        if result == 'd':
            results[0] += 1
        elif result == 'w':
            results[1] += 1
        else:
            results[2] += 1   

    return results

def parallelGame(queue, game_id, black_player, white_player):
    
    game = Game(False, 8, False, [black_player, white_player])
    winning_player = game.run()
    queue.put(winning_player)
    # print('Parallel completed game %s on process: %s' %(str(game_id), str(mp.current_process())))

if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description='Testing env for othello agents')
    parser.add_argument('-n', dest='number_of_games', action='store',
                        nargs=1, default=['1'], help='The number of games to \
                        run, used for analysis.')
    parser.add_argument('-pD', dest='dark_player', type=str, default='r', 
                        help='Type of player to use dark pieces.')
    parser.add_argument('-pW', dest='white_player', type=str, default='r', 
                        help='Type of player to use white pieces.')

    args = parser.parse_args()
    num_of_games = int(args.number_of_games[0])
    black_player = args.dark_player
    white_player = args.white_player 

    
    # serial_time_start = time.time()
    # serial_results = runSerialGames()
    # serial_time_taken = time.time() - serial_time_start

    parallel_time_start = time.time()
    parallel_results = runParallelGames(num_of_games, black_player, white_player)
    parallel_time_taken = time.time()- parallel_time_start

    print(
        'Number of games: %s | Black player: %s | White player: %s \n\
Parallel time: %d'\
        % (num_of_games, black_player, white_player, parallel_time_taken)
    )
    print('\nResults:')
    print('Black wins:', parallel_results[0])
    print('White wins:', parallel_results[1])
    print('Draws:', parallel_results[2])