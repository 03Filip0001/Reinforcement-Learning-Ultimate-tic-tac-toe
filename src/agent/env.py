import copy

from src.XO.board import Board
from src.XO.cell import CellValues
from src.agent.encoding import index_to_action, legal_action_mask, encode_state


class UltimateTTTEnv:
    def __init__(self):
        self.board = Board()
        self.current_player = CellValues.X
        self.next_board_pos = None
        self.done = False
        self.winner = CellValues.EMPTY

    def reset(self):
        self.board = Board()
        self.current_player = CellValues.X
        self.next_board_pos = None
        self.done = False
        self.winner = CellValues.EMPTY
        return encode_state(self.board, self.current_player, self.next_board_pos)

    def clone(self):
        return copy.deepcopy(self)

    def legal_actions(self):
        return legal_action_mask(self.board, self.next_board_pos)

    def is_terminal(self):
        return self.done

    def step(self, action_index):
        if self.done:
            raise ValueError("Game is already finished.")

        big_coords, small_coords = index_to_action(action_index)
        player = self.current_player
        valid, next_big_coords = self.board.play(big_coords, small_coords, self.next_board_pos, player)
        if not valid:
            raise ValueError("Illegal move selected.")

        self.next_board_pos = next_big_coords
        self.winner = self.board.checkWinner()
        if self.winner != CellValues.EMPTY:
            self.done = True

        reward = 0.0
        if self.done:
            if self.winner == CellValues.DRAW:
                reward = 0.0
            elif self.winner == player:
                reward = 1.0
            else:
                reward = -1.0

        self.current_player = CellValues.O if player == CellValues.X else CellValues.X
        state = encode_state(self.board, self.current_player, self.next_board_pos)
        return state, reward, self.done, self.winner
