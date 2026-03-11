import time

import dearpygui.dearpygui as dpg
import numpy as np

from engine.game import GameOfLife

DRAWLIST_TAG = "drawlist_board"
BOARD_WIDTH = 200
BOARD_HEIGHT = 200

def draw_board(board: np.ndarray, width: int, height: int) -> None:
    cell_width = float(width) / board.shape[0]
    cell_height = float(height) / board.shape[1]
    #print(board)
    dpg.delete_item(DRAWLIST_TAG, children_only=True)
    dpg.draw_rectangle((0,0), (width,height), color=(255,255,255), fill=(255,255,255), parent=DRAWLIST_TAG)
    living_cells = np.where(board == True)
    living_cells = np.column_stack((living_cells[1], living_cells[0]))
    for row, col in living_cells:
        dpg.draw_rectangle((cell_width*row, cell_height*col), (cell_width*(row+1), cell_height*(col+1)), color=(0, 0, 0), fill=(0, 0, 0),parent=DRAWLIST_TAG)
    for row in range(board.shape[0]+1):
        dpg.draw_line((cell_width * row, 0), (cell_width * row, height), color=(0, 0, 0),parent=DRAWLIST_TAG)
    for col in range(board.shape[1] + 1):
        dpg.draw_line((0,cell_height*col), (width,cell_height*col), color=(0, 0, 0),parent=DRAWLIST_TAG)

def draw_last_board(sender, app_data, user_data):
    user_data.last_generation()
    draw_board(user_data.curr_board, width=BOARD_HEIGHT, height=BOARD_HEIGHT)

def draw_next_board(sender, app_data, user_data):
    user_data.next_generation()
    draw_board(user_data.curr_board, width=BOARD_HEIGHT, height=BOARD_HEIGHT)

def run_game(sender, app_data, user_data):
    while dpg.get_value(sender):
        user_data.next_generation()
        draw_board(user_data.curr_board, width=BOARD_HEIGHT, height=BOARD_HEIGHT)
        time.sleep(0.1)

def clear_board(sender, app_data, user_data):
    user_data.clear_board()
    draw_board(user_data.curr_board, width=BOARD_HEIGHT, height=BOARD_HEIGHT)

def random_reset(sender, app_data, user_data):
    user_data.reset_board()
    draw_board(user_data.curr_board, width=BOARD_HEIGHT, height=BOARD_HEIGHT)
    print(user_data.curr_board.shape, user_data.rows, user_data.cols)

def new_board(sender, app_data, user_data):
    new_rows = dpg.get_value("input_rows")
    new_cols = dpg.get_value("input_cols")
    user_data.change_size(new_rows, new_cols)
    draw_board(user_data.curr_board, width=BOARD_HEIGHT, height=BOARD_HEIGHT)
    print(user_data.rows, user_data.cols)

def main():
    # always first command
    dpg.create_context()

    game: GameOfLife = GameOfLife(8,5)


    with dpg.window(tag="Primary Window"):
        with dpg.group():
            dpg.add_text("Conway's Game of Life")
            dpg.add_text("Links: Board.\t Rechts: Einstellungen.")
            dpg.add_separator()

        with dpg.group(horizontal=True):
            # Links: Spielfeld-Container
            with dpg.child_window(width=300, height=300, border=True):
                #BOARD_WIDTH = dpg.get_item_parent()
                dpg.add_drawlist(tag=DRAWLIST_TAG, width=BOARD_WIDTH, height=BOARD_HEIGHT)
                draw_board(game.curr_board, width=BOARD_WIDTH, height=BOARD_HEIGHT)

            # Rechts: Input-Container
            with dpg.child_window(width=200, height=200, border=True):  # width=0 -> nimmt Restbreite
                dpg.add_text("CONTROLS")
                dpg.add_separator()
                dpg.add_input_int(tag="input_rows",label="Rows", default_value=20, min_value=1,min_clamped=True)
                dpg.add_input_int(tag="input_cols",label="Cols", default_value=20, min_value=1,min_clamped=True)
                dpg.add_button(label="new Board", callback=new_board, user_data=game)
                dpg.add_separator()
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Clear Board",callback=clear_board,user_data=game)
                    dpg.add_button(label="Random Reset",callback=random_reset,user_data=game)
                with dpg.group(horizontal=True):
                    dpg.add_button(tag="btn_step_back",label="<",callback=draw_last_board,user_data=game)
                    dpg.add_button(tag="btn_board_forward",label=">",callback=draw_next_board,user_data=game)
                dpg.add_checkbox(label="Run", default_value=False,callback=run_game,user_data=game)

    #window created by operating System
    dpg.create_viewport(title='Schmorv\'s Game of Life', width=600, height=600)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)

    #render loop
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()
