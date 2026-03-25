import numpy as np


class GameOfLife:
    _dtype = bool

    def __init__(
        self,
        rows: int = 30,
        cols: int = 30,
        random_start: bool = True,
        random_ones: int = None,
        board_type: str = "STANDARD",
    ) -> None:
        self.rows = rows
        self.cols = cols
        self.curr_board = np.zeros((rows, cols), dtype=self._dtype)
        if random_start:
            self.curr_board = create_random_board(
                rows=rows,
                cols=cols,
                type_value=self._dtype,
                random_ones=random_ones,
            )

        self.history = []
        self.generation = 0
        self.random_start = random_start
        self.board_type = "TORUS" if board_type == "TORUS" else "STANDARD"

    def change_board(self, board_type: str) -> None:
        self.board_type = "TORUS" if board_type == "TORUS" else "STANDARD"

    def change_size(self, new_rows: int, new_cols: int) -> None:
        if new_rows == self.rows and new_cols == self.cols:
            return

        new = np.zeros((new_rows, new_cols), dtype=self._dtype)
        min_rows = min(self.rows, new_rows)
        min_cols = min(self.cols, new_cols)
        new[0:min_rows, 0:min_cols] = self.curr_board[0:min_rows, 0:min_cols]

        self.curr_board = new
        self.rows = new_rows
        self.cols = new_cols
        self.history = []
        self.generation = 0

    def toggle_cell(self, row: int, col: int) -> None:
        self.curr_board[row, col] = not self.curr_board[row, col]
        self.history = []
        self.generation = 0

    @classmethod
    def create_from_board(cls, board: np.ndarray) -> "GameOfLife":
        obj = cls(rows=board.shape[0], cols=board.shape[1], random_start=False)
        obj.curr_board = np.array(board, dtype=cls._dtype, copy=True)
        return obj

    def next_generation(self) -> None:
        if np.count_nonzero(self.curr_board) == 0:
            return

        if self.board_type == "TORUS":
            neighbours = self._count_neighbours_torus_vectorized(self.curr_board)
        else:
            neighbours = self._count_neighbours_standard_vectorized(self.curr_board)

        next_board = (neighbours == 3) | (self.curr_board & (neighbours == 2))

        self.history.append(self.curr_board.copy())
        self.curr_board = next_board.astype(self._dtype)
        self.generation += 1

    @staticmethod
    def _count_neighbours_torus_vectorized(board: np.ndarray) -> np.ndarray:
        neighbours = np.zeros_like(board, dtype=np.int8)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                neighbours += np.roll(np.roll(board, dx, axis=0), dy, axis=1)
        return neighbours

    @staticmethod
    def _count_neighbours_standard_vectorized(board: np.ndarray) -> np.ndarray:
        padded = np.pad(board.astype(np.int8), 1, mode="constant", constant_values=0)
        return (
            padded[:-2, :-2]
            + padded[:-2, 1:-1]
            + padded[:-2, 2:]
            + padded[1:-1, :-2]
            + padded[1:-1, 2:]
            + padded[2:, :-2]
            + padded[2:, 1:-1]
            + padded[2:, 2:]
        )

    def is_cell_alive_next_gen(self, idx: int, idy: int) -> int:
        if self.board_type == "TORUS":
            living_neighbours = self.count_living_neighbours_torus(idx, idy)
        else:
            living_neighbours = self.count_living_neighbours(idx, idy)

        if living_neighbours == 2:
            return int(self.curr_board[idx, idy])
        if living_neighbours == 3:
            return 1
        return 0

    def count_living_neighbours_torus(self, idx: int, idy: int) -> int:
        left_idx = idx - 1
        right_idx = idx + 1
        up_idy = idy - 1
        down_idy = idy + 1
        living_neighbours = 0

        for x in range(left_idx, right_idx + 1):
            wrapped_x = 0 if x == self.rows else x
            for y in range(up_idy, down_idy + 1):
                wrapped_y = 0 if y == self.cols else y
                if wrapped_x != idx or wrapped_y != idy:
                    if self.curr_board[wrapped_x, wrapped_y] == 1:
                        living_neighbours += 1

        return living_neighbours

    def count_living_neighbours(self, idx: int, idy: int) -> int:
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
        if not self.history:
            return
        self.generation -= 1
        self.curr_board = self.history.pop()

    def clear_board(self) -> None:
        self.curr_board = np.zeros((self.rows, self.cols), dtype=self._dtype)
        self.generation = 0
        self.history.clear()

    def reset_board(self, random_ones: int = None) -> None:
        self.clear_board()
        self.curr_board = create_random_board(
            rows=self.rows,
            cols=self.cols,
            random_ones=random_ones,
            type_value=self._dtype,
        )


def no_living_cells(board: np.ndarray) -> bool:
    return np.count_nonzero(board) == 0


def create_random_board(
    rows: int,
    cols: int,
    type_value: type,
    random_ones: int = None,
) -> np.ndarray:
    if random_ones is None:
        random_ones = rows * cols // 3
    elif not 0 <= random_ones <= (rows * cols):
        raise ValueError("random_ones must be between 0 and rows * cols")

    flat_board = np.zeros((rows * cols,), dtype=type_value)
    if random_ones > 0:
        chosen_indices = np.random.choice(rows * cols, size=random_ones, replace=False)
        flat_board[chosen_indices] = 1

    return flat_board.reshape((rows, cols))
