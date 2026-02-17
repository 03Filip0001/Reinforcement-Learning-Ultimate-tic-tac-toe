from enum import Enum, auto

from src.XO.cell import CellValues

from src.agent.agent import TrainedAgent

class PlayerType(Enum):
    HUMAN = auto()
    AGENT = auto()

class Player:
    def __init__(self, player: CellValues, playerType: PlayerType, modelPath: str  = ""):
        self.player: CellValues = player
        self.type: PlayerType = playerType
        
        if self.type == PlayerType.AGENT:
            self.action = TrainedAgent(str(modelPath))
        
    def getType(self):
        return self.type
    
    def getPlayer(self):
        return self.player
    
    def play(self, board, currentPlayer, nextBoardPos):
        return self.action.select_move(board, currentPlayer, nextBoardPos)