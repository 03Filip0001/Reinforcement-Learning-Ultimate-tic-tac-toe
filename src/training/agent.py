import copy
import numpy as np
import torch

from src.XO.cell import CellValues
# from src.training.env import UltimateTTTEnv
from src.gameEnvironment import GameEnvironment
from src.training.mcts import MCTS
from src.training.model import AlphaZeroNet
from src.training.encoding import index_to_action


class TrainedAgent:
    def __init__(self, model_path, mcts_simulations=100, device="cpu"):
        self.device = torch.device(device)
        self.model = AlphaZeroNet().to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
        self.mcts = MCTS(
            self.model,
            n_simulations=mcts_simulations,
            device=str(self.device),
            dirichlet_epsilon=0.0,
        )

    def select_move(self, board, current_player, next_board_pos):
        env = GameEnvironment()
        env.board = copy.deepcopy(board)
        env.setPlayer(current_player)
        env.nextBoardPos = next_board_pos
        env.running = True
        env.winner = CellValues.EMPTY

        policy = self.mcts.run(env, add_dirichlet=False)
        action = int(np.argmax(policy))
        return index_to_action(action)
