import time

import dearpygui.dearpygui as dpg
import numpy as np

from engine.game import GameOfLife

PRIMARY_WINDOW = "Primary Window"
HEADER_TEXT = "Header Text"
GAME_DISPLAY = "Game Display"
BOARD = "Board Display"
CONTROLS = "Control Panel"
DRAWLIST = "Drawlist Board"


def draw_board(board: np.ndarray) -> None:
    width,height = dpg.get_item_rect_size(BOARD)
    if width == 0 or height == 0:
        return
    colors = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "gray": (128, 128, 128),
    }

    rows, cols = board.shape
    cell_width = float(width) / cols
    cell_height = float(height) / rows

    dpg.delete_item(DRAWLIST, children_only=True)

    dpg.set_item_width(DRAWLIST, width)
    dpg.set_item_height(DRAWLIST, height)

    dpg.draw_rectangle((0, 0), (width, height), color=colors["white"], fill=colors["white"], parent=DRAWLIST)

    # draw horizontal lines
    for row in range(rows - 1):
        row += 1
        dpg.draw_line((0, cell_height * row), (width, cell_height * row), color=colors["gray"], parent=DRAWLIST)
        # draw vertical lines
    for col in range(cols - 1):
        col += 1
        dpg.draw_line((cell_width * col, 0), (cell_width * col, height), color=colors["gray"], parent=DRAWLIST)

    living_cells = np.where(board)
    living_cells = np.column_stack((living_cells[1], living_cells[0]))

    for row, col in living_cells:
        dpg.draw_rectangle((cell_width * row, cell_height * col), (cell_width * (row + 1), cell_height *
                           (col + 1)), color=colors["gray"], fill=colors["black"], parent=DRAWLIST)




def initialize_layout(game: GameOfLife) -> None:
    apply_layout()
    draw_board(game.curr_board)


def draw_last_board(sender, app_data, user_data):
    user_data.last_generation()
    draw_board(user_data.curr_board)


def draw_next_board(sender, app_data, user_data):
    user_data.next_generation()
    draw_board(user_data.curr_board)
    change_gen_counter(sender, app_data, user_data)


def run_game(sender, app_data, user_data):
    while dpg.get_value(sender):
        user_data.next_generation()
        draw_board(user_data.curr_board)
        change_gen_counter(sender, app_data, user_data)
        time.sleep(0.1)


def clear_board(sender, app_data, user_data):
    user_data.clear_board()
    draw_board(user_data.curr_board)
    change_gen_counter(sender, app_data, user_data)


def random_reset(sender, app_data, user_data):
    user_data.reset_board()
    draw_board(user_data.curr_board)
    change_gen_counter(sender, app_data, user_data)


def new_board(sender, app_data, user_data):
    new_rows = dpg.get_value("input_rows")
    new_cols = dpg.get_value("input_cols")
    user_data.change_size(new_rows, new_cols)
    draw_board(user_data.curr_board)


def change_gen_counter(sender, app_data, user_data):
    dpg.set_value("gen_counter", f"Generation: {user_data.generation}")


def get_item_config(sender, app_data, user_data):
    print(dpg.get_item_configuration(BOARD_DISPLAY))
    y = dpg.get_item_rect_size(GAME_DISPLAY)
    z = dpg.get_item_rect_size(BOARD_DISPLAY)
    print(y,z)


def apply_layout(sender,app_data,user_data) -> None:
    game_display_size = dpg.get_item_rect_size(GAME_DISPLAY)
    control_size = dpg.get_item_rect_size(CONTROLS)
    board_size = game_display_size[0] - control_size[0]
    dpg.set_item_width(BOARD, board_size)
    #draw_board(user_data.curr_board)
    next_frame = dpg.get_frame_count() + 1
    dpg.set_frame_callback(next_frame, redraw_board_after_layout,user_data=user_data.curr_board)

def redraw_board_after_layout(sender,app_data,user_data) -> None:
    draw_board(user_data)


def main():
    # always first command
    dpg.create_context()

    game: GameOfLife = GameOfLife(20, 20)

    with dpg.window(tag=PRIMARY_WINDOW):
        with dpg.group(tag=HEADER_TEXT,indent=0):
            dpg.add_text("Conway's Game of Life")
            dpg.add_text("Links: Board.\t Rechts: Einstellungen.")
            dpg.add_separator()

        with dpg.child_window(tag=GAME_DISPLAY,autosize_x=True,autosize_y=True,border=False):
            with dpg.group(horizontal=True,horizontal_spacing=0):
                with dpg.child_window(tag=CONTROLS, border=False,auto_resize_x=True):
                    dpg.add_text("CONTROLS")
                    dpg.add_text(tag="gen_counter", default_value=f"Generation: {game.generation}")
                    dpg.add_separator()
                    dpg.add_input_int(tag="input_rows", label="Rows", default_value=20, min_value=1, min_clamped=True,width=100)
                    dpg.add_input_int(tag="input_cols", label="Cols", default_value=20, min_value=1, min_clamped=True,width=100)
                    dpg.add_button(label="new Board", callback=new_board, user_data=game)
                    dpg.add_separator()
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Clear Board", callback=clear_board, user_data=game)
                        dpg.add_button(label="Random Reset", callback=random_reset, user_data=game)
                    with dpg.group(horizontal=True):
                        dpg.add_button(tag="btn_step_back", label="<", callback=draw_last_board, user_data=game)
                        dpg.add_button(tag="btn_board_forward", label=">", callback=draw_next_board, user_data=game)
                        dpg.add_button(tag="debug_print", label="<", callback=get_item_config, user_data=game)
                    dpg.add_checkbox(label="Run", default_value=False, callback=run_game, user_data=game)
                with dpg.child_window(tag=BOARD, auto_resize_x=True,track_offset=0,border=False):
                    dpg.add_drawlist(tag=DRAWLIST, width=100, height=100)
                    draw_board(game.curr_board)




    dpg.create_viewport(title='Schmorv\'s Game of Life', width=800, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window(PRIMARY_WINDOW, True)

    dpg.show_item_registry()
    dpg.set_viewport_resize_callback(apply_layout,user_data=game)
    dpg.set_frame_callback(3, apply_layout,user_data=game)
    dpg.start_dearpygui()

    dpg.destroy_context()


if __name__ == "__main__":
    main()
