from enum import Enum, auto

from src.XO.cell import CellValues

class PlayerType(Enum):
    HUMAN = auto()
    AGENT = auto()

class Player:
    def __init__(self, player: CellValues, playerType: PlayerType):
        self.player: CellValues = player
        self.type: PlayerType = playerType
        
    def getType(self):
        return self.type
    
    def getPlayer(self):
        return self.player
    
    def play(self):
        pass