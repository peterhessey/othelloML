'''
Main python module. Parses arguments and initialises an othello game.
'''

import argparse
import time
import matplotlib.pyplot as plt

from Othello import Game


def playerStringError():
    """Simple error message displayed on invalid players input
    
    """

    print('Invalid player string.')
    print('Valid players are:')
    print('Human player: h')
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
            valid_chars = ['h', 'r', 'R', 'M', 'M10', 'M30', 'C']
        else:
            valid_chars = ['h', 'r', 'M', 'M10', 'M30']

        
        if dark_player not in valid_chars or white_player not in valid_chars:
            valid_arguments = False
            playerStringError()
    
    return valid_arguments

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

    if args.verbose:
        verbose = True

    if validateArgs(args):
        if verbose:
            print('Running new othello game with the following:')
            print('Board size: %s' % args.size)
            print('Players: %s' % args.players)
            print('------------------------------')

        dark_wins = 0
        white_wins = 0
        draws = 0

        start_time = time.time()

        verbose = args.verbose
        board_size = args.size
        demo_mode = args.demo
        player_strings = [args.dark_player, args.white_player]

        for _ in range(int(args.number_of_games[0])):

            game = Game(verbose, board_size, demo_mode, player_strings)

            winning_player = game.run()

            if winning_player == 'w':
                white_wins += 1
            elif winning_player == 'd':
                dark_wins += 1
            else:
                draws += 1
        
        end_time = time.time()
        time_taken = end_time - start_time

        print('Dark - %d | White - %d | Draws - %d' % (dark_wins, white_wins, 
                                                       draws))
        print('Time taken: %s seconds' % round(time_taken, 3))
        


