import unittest

import numpy as np

from engine.game import GameOfLife, create_random_board


class TestGameOfLifeEngine(unittest.TestCase):
    def test_create_random_board_respects_random_ones(self):
        board = create_random_board(rows=5, cols=6, type_value=bool, random_ones=7)
        self.assertEqual(board.shape, (5, 6))
        self.assertEqual(np.count_nonzero(board), 7)

    def test_blinker_oscillator_standard(self):
        game = GameOfLife(rows=5, cols=5, random_start=False, board_type="STANDARD")
        game.curr_board = np.array(
            [
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            dtype=bool,
        )

        game.next_generation()

        expected = np.array(
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            dtype=bool,
        )
        self.assertTrue(np.array_equal(game.curr_board, expected))
        self.assertEqual(game.generation, 1)

    def test_last_generation_restores_previous_board(self):
        game = GameOfLife(rows=4, cols=4, random_start=False)
        game.curr_board[1, 1] = True
        game.curr_board[1, 2] = True
        game.curr_board[2, 1] = True

        before = game.curr_board.copy()
        game.next_generation()
        game.last_generation()

        self.assertTrue(np.array_equal(game.curr_board, before))
        self.assertEqual(game.generation, 0)

    def test_change_size_keeps_overlap(self):
        game = GameOfLife(rows=2, cols=2, random_start=False)
        game.curr_board = np.array([[1, 0], [0, 1]], dtype=bool)

        game.change_size(3, 4)

        self.assertEqual(game.curr_board.shape, (3, 4))
        self.assertTrue(game.curr_board[0, 0])
        self.assertTrue(game.curr_board[1, 1])


if __name__ == "__main__":
    unittest.main()
