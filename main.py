'''
Main python module. Parses arguments and initialises an othello game.
'''

import argparse
import time
import multiprocessing as mp
import matplotlib.pyplot as plt

from Othello import Game


def playerStringError():
    """Simple error message displayed on invalid players input
    
    """

    print('Invalid player string.')
    print('Valid players are:')
    print('Human player: h')
    print('Wendy: W')
    print('Computer player: c')
    print('Monte Carlo player: M')
    print('Random player: R')
    print('Roxanne player: r (board size 8 only)')
    print('CNN plyer: C (board size 8 only)')
    print('------------------------------')


def boardSizeError(board_size):
    """Simple error message displayed on invalid board size input
    
    Arguments:
        board_size {Int} -- Input board size
    """
    print('Invalid board size.')
    print('Input board size: %d' % board_size)
    print('Size must be an even integer >= 4.')
    print('------------------------------')


def validateArgs(args):
    """Validates input arguments
    
    Arguments:
        args {Namspace} -- Stores the parsed input arguments
    
    Returns:
        Bool -- Whether arguments are valid.
    """

    valid_arguments = True

    board_size = args.size
    dark_player = args.dark_player
    white_player = args.white_player

    if board_size < 4 or board_size % 2 != 0:
        boardSizeError(board_size)
        valid_arguments = False
        
    else:
        if board_size == 8:
            valid_chars = ['h', 'W', 'r', 'R', 'M', 'M10', 'M30', 'C']
        else:
            valid_chars = ['h', 'r', 'M', 'M10', 'M30']

        
        if dark_player not in valid_chars or white_player not in valid_chars:
            valid_arguments = False
            playerStringError()
    
    return valid_arguments

def extractArgs(args):

    verbose = args.verbose
    board_size = args.size
    demo_mode = args.demo
    player_strings = [args.dark_player, args.white_player]
    number_of_games = int(args.number_of_games[0])

    return verbose, board_size, demo_mode, player_strings, number_of_games


def runGame(queue, verbose, board_size, demo_mode, player_strings):

    if queue:

        print('Running game on process: ' + str(mp.current_process()))
        game = Game(verbose, board_size, False, player_strings)
        winning_player = game.run()
        queue.put(winning_player)

    else:
        game = Game(verbose, board_size, True, player_strings)
        winning_player = game.run()
        if winning_player == 'b':
            print('black wins!')
        elif winning_player == 'w':
            print('white wins!')
        else:
            print('It was a draw!')


if __name__ == "__main__":
    """Main startup, parses arguments and validates them before starting
    the game.
    """

    verbose = False

    parser = argparse.ArgumentParser(description='Run an othello game!')
    parser.add_argument('-v', dest='verbose', action='store_const',
                        const=True, default=False, help='Make the program \
                        verbose.')
    parser.add_argument('-d', dest='demo', action='store_const',
                        const=True, default=False, help='Demo mode, displays \
                        the board using pygame even without a human player.')
    parser.add_argument('-s', dest='size', action='store',
                        nargs=1, default=['8'],
                        help='The size of the board, even and >= 4 | \
                        Default = 8')
    parser.add_argument('-n', dest='number_of_games', action='store',
                        nargs=1, default=['1'], help='The number of games to \
                        run, used for analysis.')
    parser.add_argument('-pD', dest='dark_player', type=str, default='h', 
                        help='Type of player to use dark pieces.')
    parser.add_argument('-pW', dest='white_player', type=str, default='h', 
                        help='Type of player to use white pieces.')


    args = parser.parse_args()
    args.size = int(args.size[0])

    if validateArgs(args):
        
        verbose, board_size, demo_mode, player_strings, number_of_games = extractArgs(args)

        if verbose:
            print('Running new othello game with the following:')
            print('Board size: %s' % board_size)
            print('Players: %s' % player_strings)
            print('------------------------------')  

        
        if number_of_games > 1:
            
            queue = mp.Queue()
            parallel_args = (queue, verbose, board_size, demo_mode, player_strings)
            
            processes = [mp.Process(target=runGame, args=parallel_args) for _ in range(number_of_games)]

            for p in processes:
                p.start()

            for p in processes:
                p.join()


            results = [0,0,0] # black, white, draw
            for _ in range(number_of_games):
                result = queue.get()
                if result == 'd':
                    results[0] += 1
                elif result == 'w':
                    results[1] += 1
                else:
                    results[2] += 1               

            print('Black - %s, White - %s, Draws - %s' % (results[0],
                                                          results[1],
                                                          results[2]))

        else:
            runGame(None, verbose, board_size, demo_mode, player_strings)