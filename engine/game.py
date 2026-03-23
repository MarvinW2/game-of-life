import numpy
import numpy as np


class GameOfLife:
    _dtype = bool
    board_type = str

    def __init__(self, rows: int = 30, cols: int = 30, random_start: bool = True, random_ones: int = None, board_type: str = "STANDARD") -> None:
        self.curr_board = np.zeros((rows, cols), dtype=self._dtype)
        if random_start:
            self.curr_board = create_random_board(rows=rows, cols=cols, type_value=self._dtype, random_ones=random_ones)
        self.rows = rows
        self.cols = cols
        self.history = list()
        self.generation = 0
        self.random_start = random_start
        self.board_type = "TORUS" if board_type == "TORUS" else "STANDARD"

    def change_board(self, board_type :str) -> None:
        self.board_type = "TORUS" if board_type == "TORUS" else "STANDARD"

    def change_size(self, new_rows: int, new_cols: int) -> None:
        if new_rows == self.rows and new_cols == self.cols:
            return
        self.history = list()
        self.generation = 0

        new = np.zeros((new_rows, new_cols), dtype=self._dtype)

        min_rows = min(self.rows, new_rows)
        min_cols = min(self.cols, new_cols)

        new[0:min_rows, 0:min_cols] = self.curr_board[0:min_rows, 0:min_cols].copy()

        self.curr_board = new
        self.rows = new_rows
        self.cols = new_cols

    def toggle_field(self, row, col) -> None:
        self.curr_board[row, col] = not self.curr_board[row, col]
        self.history = list()
        self.generation = 0

    @classmethod
    def create_from_board(cls, board: np.ndarray) -> GameOfLife:
        obj = cls()
        obj.curr_board = board
        obj.rows, obj.cols = board.shape
        return obj

    def next_generation(self) -> None:
        uniques = np.unique(self.curr_board)
        if uniques.size == 1 and uniques[0] == 0:
            return
        # Vectorize the cell alive check for all cells at once
        is_cell_alive_func = np.vectorize(self.is_cell_alive_next_gen)

        indices_x, indices_y = np.meshgrid(np.arange(self.rows), np.arange(self.cols), indexing='ij')

        next_board = is_cell_alive_func(indices_x, indices_y)

        self.history.append(self.curr_board.copy())
        self.curr_board = next_board.astype(self._dtype)
        self.generation += 1

    def is_cell_alive_next_gen(self, idx: int, idy: int) -> int:
        if self.board_type == "TORUS":
            living_neighbours = self.count_living_neighbours_torus(idx, idy)
        else:
            living_neighbours = self.count_living_neighbours(idx, idy)
        if living_neighbours == 2:
            return self.curr_board[idx, idy]
        elif living_neighbours == 3:
            return 1
        return 0

    def count_living_neighbours_torus(self, idx: int, idy: int) -> int:
        left_idx = idx - 1
        right_idx = idx + 1
        up_idy = idy - 1
        down_idy = idy + 1
        living_neighbours = 0
        for x in range(left_idx, right_idx + 1):
            if x == self.rows:
                x = 0
            for y in range(up_idy, down_idy + 1):
                if y == self.cols:
                    y = 0
                if x != idx or y != idy:
                    if self.curr_board[x, y] == 1:
                        living_neighbours += 1
        return living_neighbours

    def count_living_neighbours(self, idx: int, idy: int) -> int:
        # neighbors indices
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
        if len(self.history) == 0:
            return
        self.generation -= 1
        self.curr_board = self.history.pop()

    def clear_board(self) -> None:
        self.curr_board = np.zeros((self.rows, self.cols), dtype=self._dtype)
        self.generation = 0
        self.history.clear()

    def reset_board(self,random_ones: int) -> None:
        self.clear_board()
        if random_ones:
            self.curr_board = create_random_board(rows=self.rows, cols=self.cols, random_ones=random_ones, type_value=self._dtype)
        else:
            self.curr_board = create_random_board(rows=self.rows, cols=self.cols, type_value=self._dtype)

    def toggle_cell(self, row: int, col: int) -> None:
        self.curr_board[row, col] = not self.curr_board[row, col]


def no_living_cells(board: np.ndarray) -> bool:
    return len(np.where(board == 1)) == 0

def create_random_board(rows: int, cols: int, type_value: type, random_ones: int = None):
    if not random_ones:
        random_ones = rows * cols // 3
    elif not 0 < random_ones <= (rows * cols):
        raise ValueError('random_ones must be between 0 and rows * cols')
    board = np.zeros((rows, cols), dtype=type_value)
    for i in range(random_ones):
        row, col = np.random.randint(0, rows), np.random.randint(0, cols)
        if board[row, col] == 0:
            board[row, col] = 1
        else:
            i -= 1
    return board
