import argparse

def playerStringError(players_string):
    print("Invalid player string. Input string: %s" % players_string)
    print('Please only enter 2 characters. Valid players are:')
    print('Human player: h')
    print('Computer player: c')

def boardSizeError(board_size):
    print('Invalid board size.')
    print('Input board size: %d' % board_size)
    print('Size must be an even integer >= 4.')


if __name__ == "__main__":

    verbose = False
    valid_arguments = True

    parser = argparse.ArgumentParser(description='Run an othello game!')
    parser.add_argument('-v', dest='verbose', action='store_const',
                        const=True, default=False, help='Make the program \
                        verbose.')
    parser.add_argument('-s', dest='size', action='store',
                        nargs=1, default=8,
                        help='The size of the board, even and >= 4 | \
                        Default = 8')
    parser.add_argument('-p', dest='players', action='store', nargs = 1, 
                        default='hc', help='The type of players, passed \
                        as a 2 character string, e.g. "hc" for human v \
                        computer, "cc" for computer v computer or "hh" for \
                        human vs human | Default = hc')



    args = parser.parse_args()
    if args.verbose:
        verbose = True

    if verbose:
        print('Running new othello game with the following:')
        print('Board size: %s' % args.size[0])
        print('Players: %s' % args.players[0])
        print('------------------------------')

    board_size = int(args.size[0])
    players_string = args.players[0]

    if board_size < 4 or board_size % 2 != 0:
        boardSizeError(board_size)
        valid_arguments = False

    if len(players_string) != 2:
        valid_arguments = False
        playerStringError(players_string)
        
    else:
        valid_chars = 'hc'
        for each player_char in players_string:
            if player_char not in valid_chars:
                valid_arguments = False
                playerStringError(players_string)
    

        


