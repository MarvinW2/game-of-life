from math import gamma

import numpy as np

class GameOfLife:
    _dtype = bool

    def __init__(self,rows: int = 30, cols: int =30, random_start: bool = True, random_ones: int =None):
        self.curr_board = np.zeros((rows, cols), dtype=self._dtype)
        if random_start:
            self.curr_board = create_random_board(rows=rows, cols=cols,type_value = self._dtype, random_ones=random_ones)
        self.rows = rows
        self.cols = cols
        self.history = list[np.ndarray]()
        self.generation = 0
        self.random_start = random_start

    def change_size(self, new_rows: int, new_cols : int) -> None:
        if new_rows == self.rows and new_cols == self.cols:
            return

        new = np.zeros((new_rows, new_cols), dtype=self._dtype)

        min_rows = min(self.rows, new_rows)
        min_cols = min(self.cols, new_cols)

        new[0:min_rows, 0:min_cols] = self.curr_board[0:min_rows, 0:min_cols].copy()

        self.curr_board = new
        self.rows = new_rows
        self.cols = new_cols


    @classmethod
    def create_from_board(cls, board: np.ndarray) -> GameOfLife:
        obj = cls()
        obj.curr_board = board
        obj.rows, obj.cols = board.shape
        return obj

    def next_generation(self) -> None:
        next_board = np.zeros((self.rows,self.cols), dtype=self._dtype)
        for idx in range(0, next_board.shape[0]):
            for idy in range(0, next_board.shape[1]):
                next_board[idx, idy] = self.is_cell_alive_next_gen(idx, idy)
        self.history.append(self.curr_board)
        self.curr_board = next_board
        self.generation += 1

    def is_cell_alive_next_gen(self, idx: int, idy: int) -> int:
        living_neighbours = self.count_living_neighbours(idx, idy)
        if living_neighbours == 2:
            return self.curr_board[idx, idy]
        elif living_neighbours == 3:
            return 1
        return 0

    def count_living_neighbours(self,idx: int, idy: int) -> int:
        # neigbours indices
        left_idx = idx - 1 if idx > 0 else 0
        right_idx = idx + 1 if idx + 1 < self.rows else idx
        up_idy = idy - 1 if idy > 0 else 0
        down_idy = idy + 1 if idy + 1 < self.cols else idy
        living_neighbours = 0
        for x in range(left_idx, right_idx + 1):
            for y in range(up_idy, down_idy + 1):
                if x != idx or y != idy:
                    if self.curr_board[x, y] == 1:
                        living_neighbours += 1
        return living_neighbours

    def last_generation(self) -> None:
        if self.generation == 0:
            return
        self.generation -= 1
        self.curr_board = self.history.pop()

    def clear_board(self) -> None:
        self.curr_board = np.zeros((self.rows, self.cols), dtype=self._dtype)
        self.generation = 0
        self.history.clear()

    def reset_board(self) -> None:
        self.clear_board()
        self.curr_board = create_random_board(rows=self.rows, cols=self.cols, type_value=self._dtype)

def print_board(board: np.ndarray) -> None:
    rows, cols = board.shape
    for x in range(0, rows):
        for y in range(0, cols):
            a = board[x, y]
            print(a, " ", end="")
        print(board.dtype)
    return

def create_random_board(rows: int, cols:  int, type_value: type , random_ones: int = None):
    if not random_ones:
        random_ones = rows * cols//3
    if not 0 < random_ones <= (rows * cols):
        raise ValueError('random_ones must be between 0 and rows * cols')
    board = np.zeros((rows, cols), dtype=type_value)
    for i in range(random_ones):
        row, col = np.random.randint(0, rows), np.random.randint(0, cols)
        if board[row, col] == 0:
            board[row, col] = 1
        else:
            i -= 1
    return board
