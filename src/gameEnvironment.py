import copy
import numpy as np

from src.gameBase import GameBase
from src.XO.cell import CellValues

from src.training.encoding import index_to_action, legal_action_mask, encode_state

class GameEnvironment(GameBase):
    def __init__(self):
        super().__init__()
                            
    def clone(self):
        return copy.deepcopy(self)
    
    def legal_action(self):
        return legal_action_mask(self.board, self.nextBoardPos)
    
    def is_terminal(self):
        return not self.running
    
    def step(self, action_index):
        if not self.running:
            raise ValueError("Game is already finished")
        
        bigCoords, smallCoords = index_to_action(action_index)
        player = self.currentPlayer
        self.play(bigCoords, smallCoords, player)
        
        if not self.valid:
            raise ValueError("Illegal move selected")
        
        self.checkWinner()  # ✅ DODAJ OVO!
        
        reward = 0.0
        if not self.running:
            winner = self.winner
            if winner == CellValues.DRAW:
                reward = 0.0
            elif winner == player:
                reward = 1.0
            else:
                reward = -1.0
        
        state = encode_state(self.board, self.currentPlayer, self.nextBoardPos)
        return state, reward, self.running, self.winner