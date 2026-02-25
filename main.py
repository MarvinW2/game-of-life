# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 13:25:57 2026

@author: schmorv
"""

from gui import *
from engine import game

if __name__ == "__main__":
    board = game.create_board(10)
    board[2, 3:]=1
    print(board)
    print()
    curr_board = game.next_generation(board)
    print(curr_board)
    #print_board(board)