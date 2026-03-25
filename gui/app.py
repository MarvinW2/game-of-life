import dearpygui.dearpygui as dpg
import numpy as np

from engine.game import GameOfLife

PRIMARY_WINDOW = "Primary Window"
HEADER_TEXT = "Header Text"
GAME_DISPLAY = "Game Display"
BOARD = "Board Display"
CONTROLS = "Control Panel"
DRAWLIST = "Drawlist Board"

BOARD_RENDER_FPS = 3


def draw_board(board: np.ndarray) -> None:
    width, height = dpg.get_item_rect_size(BOARD)
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

    cell_size = min(cell_width, cell_height)
    cell_width = cell_height = cell_size

    width = cell_width * cols
    height = cell_height * rows

    dpg.delete_item(DRAWLIST, children_only=True)

    dpg.set_item_width(DRAWLIST, width)
    dpg.set_item_height(DRAWLIST, height)

    dpg.draw_rectangle((0, 0), (width, height), color=colors["white"], fill=colors["white"], parent=DRAWLIST)

    # draw horizontal lines
    for row in range(1, rows):
        y = cell_height * row
        dpg.draw_line((0, y), (width, y), color=colors["gray"], parent=DRAWLIST)

    # draw vertical lines
    for col in range(1, cols):
        x = cell_width * col
        dpg.draw_line((x, 0), (x, height), color=colors["gray"], parent=DRAWLIST)

    living_cells = np.argwhere(board)

    for row, col in living_cells:
        dpg.draw_rectangle((cell_width * row, cell_height * col), (cell_width * (row + 1), cell_height *
                           (col + 1)), color=colors["gray"], fill=colors["black"], parent=DRAWLIST)

    if len(living_cells) == 0:
        dpg.draw_text((width // 2 - 30, height // 2 - 30), "ENDE", color=(250, 0, 0), size=30, parent=DRAWLIST)


def initialize_layout(sender, app_data, game: GameOfLife) -> None:
    apply_layout(sender, app_data, user_data=game)
    draw_board(game.curr_board)


def draw_last_board(sender, app_data, user_data: GameOfLife) -> None:
    user_data.last_generation()
    draw_board(user_data.curr_board)
    change_gen_counter(user_data)


def draw_next_board(sender, app_data, user_data: GameOfLife) -> None:
    user_data.next_generation()
    draw_board(user_data.curr_board)
    change_gen_counter(user_data)


def run_game(sender, app_data, user_data: GameOfLife) -> None:
    if dpg.get_value("checkbox_run"):
        user_data.next_generation()
        # apply_layout(sender,app_data,user_data)
        draw_board(user_data.curr_board)
        change_gen_counter(user_data)
        fps = max(dpg.get_frame_rate(), 1.0)
        frames_per_step = max(1, int(fps // BOARD_RENDER_FPS))
        dpg.set_frame_callback(dpg.get_frame_count() + frames_per_step, run_game, user_data=user_data)


def clear_board(sender, app_data, user_data: GameOfLife) -> None:
    user_data.clear_board()
    draw_board(user_data.curr_board)
    change_gen_counter(user_data)


def random_reset(sender, app_data, user_data: GameOfLife) -> None:
    x = dpg.get_value("input_living")
    user_data.reset_board(x)
    draw_board(user_data.curr_board)
    change_gen_counter(user_data)


def change_board_size(sender, app_data, user_data: GameOfLife) -> None:
    new_rows = dpg.get_value("input_rows")
    new_cols = dpg.get_value("input_cols")
    user_data.change_size(new_rows, new_cols)
    draw_board(user_data.curr_board)
    change_gen_counter(user_data)


def change_cell(sender, app_data, user_data: GameOfLife) -> None:
    x = dpg.get_drawing_mouse_pos()
    width, height = dpg.get_item_rect_size(BOARD)
    if width == 0 or height == 0:
        return
    rows, cols = user_data.curr_board.shape
    cell_width = float(width) / cols
    cell_height = float(height) / rows

    cell_size = min(cell_width, cell_height)
    cell_width = cell_height = cell_size

    col, row = int(x[0] // cell_width), int(x[1] // cell_height)
    if not (0 <= row < rows and 0 <= col < cols):
        return
    user_data.toggle_cell(row, col)

    draw_board(user_data.curr_board)
    change_gen_counter(user_data)


def change_gen_counter(user_data: GameOfLife) -> None:
    dpg.set_value("gen_counter", f"Generation: {user_data.generation}")


def apply_layout(sender, app_data, user_data: GameOfLife) -> None:
    game_display_size = dpg.get_item_rect_size(GAME_DISPLAY)
    control_size = dpg.get_item_rect_size(CONTROLS)
    board_size = game_display_size[0] - control_size[0]
    dpg.set_item_width(BOARD, board_size)
    # draw_board(user_data.curr_board)
    next_frame = dpg.get_frame_count() + 1
    dpg.set_frame_callback(next_frame, redraw_board_after_layout, user_data=user_data.curr_board)


def redraw_board_after_layout(sender, app_data, user_data) -> None:
    draw_board(user_data)


def change_board_type(sender, app_data, user_data: GameOfLife) -> None:
    user_data.change_board(dpg.get_value(sender).upper())
    draw_board(user_data.curr_board)


def main() -> None:
    # always first command
    dpg.create_context()

    game: GameOfLife = GameOfLife(20, 20)

    with dpg.window(tag=PRIMARY_WINDOW):
        with dpg.group(tag=HEADER_TEXT, indent=0):
            dpg.add_text("Conway's Game of Life")
            dpg.add_text("Links: Board.\t Rechts: Einstellungen.")
            dpg.add_separator()

        with dpg.child_window(tag=GAME_DISPLAY, autosize_x=True, autosize_y=True, border=False):
            with dpg.group(horizontal=True, horizontal_spacing=0):

                with dpg.child_window(tag=CONTROLS, border=False, auto_resize_x=True):

                    dpg.add_text(tag="gen_counter", default_value=f"Generation: {game.generation}")
                    dpg.add_separator()

                    dpg.add_text("Board Size:")
                    dpg.add_input_int(
                        tag="input_rows",
                        label="Rows",
                        default_value=game.rows,
                        min_value=2,
                        min_clamped=True,
                        width=100,
                        callback=change_board_size,
                        user_data=game)
                    dpg.add_input_int(
                        tag="input_cols",
                        label="Cols",
                        default_value=game.cols,
                        min_value=2,
                        min_clamped=True,
                        width=100,
                        callback=change_board_size,
                        user_data=game)
                    dpg.add_radio_button(tag="input_board_type", items=("Standard", "Torus"), callback=change_board_type, user_data=game, horizontal=True)
                    # dpg.add_input_int(tag="input_cols", label="Cols", default_value=game.cols, min_value=2, min_clamped=True,width=100,callback=change_board_size,user_data=game)

                    dpg.add_separator()

                    dpg.add_button(tag="btn_clear", label="Clear Board", callback=clear_board, user_data=game)

                    dpg.add_separator()

                    dpg.add_text("Anzahl lebende Zellen:")
                    dpg.add_text("(nur bei Random Reset)")
                    dpg.add_input_int(tag="input_living",
                                      default_value=int(game.cols * game.rows / 3), min_value=0, min_clamped=True,
                                      width=100, user_data=game)
                    dpg.add_button(label="Random Reset", callback=random_reset, user_data=game)

                    dpg.add_separator()

                    with dpg.group(horizontal=True):
                        dpg.add_button(tag="btn_step_back", arrow=True, direction=dpg.mvDir_Left, callback=draw_last_board, user_data=game)
                        dpg.add_button(tag="btn_board_forward", arrow=True, direction=dpg.mvDir_Right, callback=draw_next_board, user_data=game)
                    dpg.add_checkbox(tag="checkbox_run", label="Run", default_value=False, callback=run_game, user_data=game)

                with dpg.child_window(tag=BOARD, auto_resize_x=False, track_offset=0, border=False):
                    dpg.add_drawlist(tag=DRAWLIST, width=0, height=0)
                    draw_board(game.curr_board)

    with dpg.item_handler_registry(tag="widget handler") as handler:

        dpg.add_item_clicked_handler(callback=change_cell, user_data=game)

    dpg.bind_item_handler_registry(DRAWLIST, "widget handler")

    with dpg.theme() as item_theme:
        with dpg.theme_component(dpg.mvAll):
            # dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (200,200,100), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (100, 200, 100), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (200, 200, 100), category=dpg.mvThemeCat_Core)

            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1)
            # dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
            dpg.add_theme_style(dpg.mvThemeCol_CheckMark, 1)

    # dpg.bind_item_theme(CONTROLS, item_theme)

    dpg.create_viewport(title='Schmorv\'s Game of Life', width=800, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window(PRIMARY_WINDOW, True)

    dpg.show_item_registry()
    dpg.set_viewport_resize_callback(apply_layout, user_data=game)
    dpg.set_frame_callback(3, apply_layout, user_data=game)
    dpg.start_dearpygui()

    dpg.destroy_context()


if __name__ == "__main__":
    main()
