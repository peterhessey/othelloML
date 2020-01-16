from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, verbose, dark_player):
        """Constructor method for the Player class
        
        Arguments:
            ABC {Object} -- Abstract Base Class object
            verbose {bool} -- Determines if player is verbose or not
            dark_player {bool} -- Determines if the player plays using the dark
            or white pieces
        """
        self.verbose = verbose
        self.dark_player = dark_player

    @abstractmethod
    def getNextBoardState(self):
        """Abstract method for getNextBoardState()
        """
        pass
