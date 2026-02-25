import numpy as np

def create_board(n: int) -> np.ndarray:
    board = np.zeros((n, n), dtype=int)
    return board

def create_random_board(n: int, random_ones:int) -> np.ndarray:
    board = np.zeros((n, n), dtype=int)
    for i in range(random_ones):
        row, col = np.random.random_integers(0, n - 1), np.random.random_integers(0, n - 1)
        if board[row, col] == 0:
            board[row, col] = 1
        else:
            i -= 1
    return board

def print_board(board: np.ndarray) -> None:
    rows, cols = board.shape
    for x in range(0, rows):
        for y in range(0, cols):
            a = board[x, y]
            print(a, " ", end="")
        print()
    return


def next_generation(curr_board: np.ndarray) -> np.ndarray:
    next_board = np.zeros(curr_board.shape, dtype=int)
    for idx in range(0, next_board.shape[0]):
        for idy in range(0, next_board.shape[1]):
            next_board[idx, idy] = is_cell_alive_next_gen(curr_board, idx, idy)
    return next_board


def is_cell_alive_next_gen(board: np.ndarray, idx: int, idy: int) -> int:
    living_neighbours = count_living_neighbours(board, idx, idy)
    if living_neighbours == 2:
        return board[idx, idy]
    elif living_neighbours == 3:
        return 1
    return 0


def count_living_neighbours(board: np.ndarray, idx: int, idy: int) -> int:
    # neigbours indices
    left_idx = idx - 1 if idx > 0 else 0
    right_idx = idx + 1 if idx + 1 < board.shape[0] else idx
    up_idy = idy - 1 if idy > 0 else 0
    down_idy = idy + 1 if idy + 1 < board.shape[1] else idy

    living_neighbours = 0
    for x in range(left_idx, right_idx + 1):
        for y in range(up_idy, down_idy + 1):
            if x != idx or y != idy:
                if board[x, y] == 1:
                    living_neighbours += 1
    return living_neighbours