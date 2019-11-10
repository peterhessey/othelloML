from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, verbose, dark_player):
        self.verbose = verbose
        self.dark_player = dark_player

    @abstractmethod
    def getNextBoardState(self):
        pass
