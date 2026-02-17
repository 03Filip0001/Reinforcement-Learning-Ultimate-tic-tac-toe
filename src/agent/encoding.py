import numpy as np

from src.XO.cell import CellValues


def _cell_to_int(v):
    if isinstance(v, CellValues):
        return v.value
    return int(v)


def action_to_index(big_col, big_row, cell_col, cell_row):
    return (big_row * 3 + big_col) * 9 + (cell_row * 3 + cell_col)


def index_to_action(index):
    big = index // 9
    cell = index % 9
    big_row, big_col = divmod(big, 3)
    cell_row, cell_col = divmod(cell, 3)
    return (big_col, big_row), (cell_col, cell_row)


def _normalized_next_board(board, next_board_pos):
    if next_board_pos is None:
        return None
    nbx, nby = next_board_pos
    if board.board[nby][nbx].checkWinner() != CellValues.EMPTY:
        return None
    return next_board_pos


def encode_state(board, current_player, next_board_pos):
    grid = board.getBoardList()  # [big_row][big_col][cell_row][cell_col]
    x_plane = np.zeros((9, 9), dtype=np.float32)
    o_plane = np.zeros((9, 9), dtype=np.float32)
    nb_plane = np.zeros((9, 9), dtype=np.float32)
    cp_plane = np.zeros((9, 9), dtype=np.float32)

    for br in range(3):
        for bc in range(3):
            for cr in range(3):
                for cc in range(3):
                    v = _cell_to_int(grid[br][bc][cr][cc])
                    r = br * 3 + cr
                    c = bc * 3 + cc
                    if v == CellValues.X.value:
                        x_plane[r][c] = 1.0
                    elif v == CellValues.O.value:
                        o_plane[r][c] = 1.0

    next_board_pos = _normalized_next_board(board, next_board_pos)
    if next_board_pos is None:
        nb_plane[:, :] = 1.0
    else:
        nbx, nby = next_board_pos
        for cr in range(3):
            for cc in range(3):
                r = nby * 3 + cr
                c = nbx * 3 + cc
                nb_plane[r][c] = 1.0

    cp_value = 1.0 if current_player == CellValues.X else 0.0
    cp_plane[:, :] = cp_value

    return np.stack([x_plane, o_plane, nb_plane, cp_plane], axis=0)


def legal_action_mask(board, next_board_pos):
    mask = np.zeros(81, dtype=np.float32)
    grid = board.getBoardList()

    next_board_pos = _normalized_next_board(board, next_board_pos)

    for br in range(3):
        for bc in range(3):
            if next_board_pos is not None and (bc, br) != next_board_pos:
                continue

            if board.board[br][bc].checkWinner() != CellValues.EMPTY:
                continue

            for cr in range(3):
                for cc in range(3):
                    v = _cell_to_int(grid[br][bc][cr][cc])
                    if v == CellValues.EMPTY.value:
                        idx = action_to_index(bc, br, cc, cr)
                        mask[idx] = 1.0

    return mask
