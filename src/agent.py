import copy
import numpy as np
import torch

from src.cell import CellValues
from src.env import UltimateTTTEnv
from src.mcts import MCTS
from src.model import AlphaZeroNet
from src.encoding import index_to_action


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
        env = UltimateTTTEnv()
        env.board = copy.deepcopy(board)
        env.current_player = current_player
        env.next_board_pos = next_board_pos
        env.done = False
        env.winner = CellValues.EMPTY

        policy = self.mcts.run(env, add_dirichlet=False)
        action = int(np.argmax(policy))
        return index_to_action(action)
