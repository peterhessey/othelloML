# Program for playing agents against one another efficiently using parallel
# programming.

import time
import math
import multiprocessing as mp
import matplotlib.pyplot as plt
import argparse
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

from Othello import Game

NUM_OF_GAMES = 5000

def runSerialGames(black_player, white_player):

    results = [0,0,0] #black, white, draws
    for i in range(NUM_OF_GAMES):
        
        game = Game(False, 8, False, [black_player, white_player])
        winning_player = game.run()
        # print('Serial completed game %d/%d' %(i+1, NUM_OF_GAMES))

        if winning_player == 'b':
            results[0] += 1
        elif winning_player == 'w':
            results[1] += 1
        else:
            results[2] += 1

    return results

def runParallelGames(black_player, white_player):

    games_played = 0
    games_per_loop = 250
    results = [0,0,0] # black, white, draw

    while games_played < NUM_OF_GAMES:
        queue = mp.Queue()
        processes = [mp.Process(target=parallelGame,
                                args=(queue, i+1, black_player, white_player))
                                for i in range(games_per_loop)]

        for p in processes:
            p.start()
        
        for p in processes:
            p.join()

        
        for _ in range(games_per_loop):
            result = queue.get()
            if result == 'd':
                results[0] += 1
            elif result == 'w':
                results[1] += 1
            else:
                results[2] += 1   
    
        games_played += games_per_loop

    return results

def parallelGame(queue, game_id, black_player, white_player):
    
    game = Game(False, 8, False, [black_player, white_player])
    winning_player = game.run()
    queue.put(winning_player)
    # print('Parallel completed game %s on process: %s' %(str(game_id), str(mp.current_process())))

if __name__=='__main__':

    print('Running %s games per value for c-val testing' % str(NUM_OF_GAMES * 2))
    results_dict = {}
    for i in range(5, 26):
        c_val = float(i/10)
        results_dict[c_val] = 0
        for j in range(2):
            if j == 0:
                black_c_val = math.sqrt(2)
                white_c_val = c_val
            else:
                black_c_val = c_val
                white_c_val = math.sqrt(2)
            
            black_player = 'Mc' + str(black_c_val)
            white_player = 'Mc' + str(white_c_val)

            # serial_time_start = time.time()
            # serial_results = runSerialGames()
            # serial_time_taken = time.time() - serial_time_start

            parallel_time_start = time.time()
            parallel_results = runParallelGames(black_player, white_player)
            parallel_time_taken = time.time()- parallel_time_start           

            if j==0:
                results_dict[c_val] += parallel_results[1]
            else:
                results_dict[c_val] += parallel_results[0]

        print('Games for c-val of %f complete' % c_val)

    print(results_dict)