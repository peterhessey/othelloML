import numpy as np
import roxanne
import human_player as human

class Game:

    def __init__(self, args):
        self.verbose = args.verbose
        self.board_size = args.size
        self.player_1, self.player_2 = self.setUpPlayers(args.players)
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

        for player_char in player_string:
            if player_char == 'h':
                new_player = human.Human(self.verbose)
            elif player_char == 'c':
                new_player = roxanne.Roxanne(self.verbose)
        
            players.append(new_player)

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


        if self.verbose:
            print("Initial board array:")
            print(board)
            
        return board
    
    def run(self):
        print("Running game woo")

        