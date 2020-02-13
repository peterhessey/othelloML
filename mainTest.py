# Program for playing agents against one another efficiently using parallel
# programming.

import time
import multiprocessing as mp
import matplotlib.pyplot as plt
import argparse
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

from Othello import Game

NUM_OF_GAMES = 4
BLACK_PLAYER = 'r'
WHITE_PLAYER = 'r'

def runSerialGames():

    results = [0,0,0] #black, white, draws
    for i in range(NUM_OF_GAMES):
        
        game = Game(False, 8, False, [BLACK_PLAYER, WHITE_PLAYER])
        winning_player = game.run()
        print('Serial completed game %d/%d' %(i+1, NUM_OF_GAMES))

        if winning_player == 'b':
            results[0] += 1
        elif winning_player == 'w':
            results[1] += 1
        else:
            results[2] += 1

    return results

def runParallelGames():
    queue = mp.Queue()
    processes = [mp.Process(target=parallelGame, args=(queue, i+1,)) for i in range(NUM_OF_GAMES)]

    for p in processes:
        p.start()
    
    for p in processes:
        p.join()

    results = [0,0,0] # black, white, draw
    for _ in range(NUM_OF_GAMES):
        result = queue.get()
        if result == 'd':
            results[0] += 1
        elif result == 'w':
            results[1] += 1
        else:
            results[2] += 1   

    return results

def parallelGame(queue, game_id):
    
    game = Game(False, 8, False, [BLACK_PLAYER, WHITE_PLAYER])
    winning_player = game.run()
    queue.put(winning_player)
    print('Parallel completed game %s on process: %s' %(str(game_id), str(mp.current_process())))

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
    NUM_OF_GAMES = int(args.number_of_games[0])
    BLACK_PLAYER = args.dark_player
    WHITE_PLAYER = args.white_player 
    
    
    # serial_time_start = time.time()
    # serial_results = runSerialGames()
    # serial_time_taken = time.time() - serial_time_start

    parallel_time_start = time.time()
    parallel_results = runParallelGames()
    parallel_time_taken = time.time()- parallel_time_start

    print(
        'Number of games: %s | Black player: %s | White player: %s \n\
Parallel time: %d'\
        % (NUM_OF_GAMES, BLACK_PLAYER, WHITE_PLAYER, parallel_time_taken)
    )
    print('\nResults:')
    print('Black wins:', parallel_results[0])
    print('White wins:', parallel_results[1])
    print('Draws:', parallel_results[2])