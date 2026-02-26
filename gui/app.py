import dearpygui.dearpygui as dpg
import numpy as np

from engine import game as eng

def draw_board(board: np.ndarray, width: int, height: int) -> None:
    cell_width = float(width) / board.shape[0]
    cell_height = float(height) / board.shape[1]
    print(width, height)
    print(board)
    with dpg.drawlist(tag="drawlist_board",width=width, height=height):
        dpg.draw_text((0, 0), "Origin", color=(0, 0, 0, 0), size=15)
        dpg.draw_rectangle((0,0), (width,height), color=(255,255,255), fill=(255,255,255))
        living_cells = np.where(board == 1)
        print(living_cells)
        #living_cells = np.array((living_cells[0],living_cells[1]))
        living_cells = np.column_stack((living_cells[1], living_cells[0]))
        for row, col in living_cells:
            dpg.draw_rectangle((cell_width*row, cell_height*col), (cell_width*(row+1), cell_height*(col+1)), color=(0, 0, 0), fill=(0, 0, 0))
        for row in range(board.shape[0]+1):
            dpg.draw_line((cell_width * row, 0), (cell_width * row, height), color=(0, 0, 0))
        for col in range(board.shape[1] + 1):
            dpg.draw_line((0,cell_height*col), (width,cell_height*col), color=(0, 0, 0))

def main():
    # always first command
    dpg.create_context()

    board: np.ndarray = eng.create_random_board(10,30)


    with dpg.window(tag="Primary Window"):
        with dpg.group():
            dpg.add_text("Conway's Game of Life")
            dpg.add_text("Links: Board.\t Rechts: Einstellungen.")
            dpg.add_separator()

        with dpg.group(horizontal=True):
            # Links: Spielfeld-Container
            with dpg.child_window(width=300, height=300, border=True):
                draw_board(board, 200-50, 300-50)

            # Rechts: Input-Container
            with dpg.child_window(width=0, height=200, border=True):  # width=0 -> nimmt Restbreite
                dpg.add_text("CONTROLS")
                dpg.add_separator()
                dpg.add_input_int(label="Rows", default_value=50, min_value=1)
                dpg.add_input_int(label="Cols", default_value=50, min_value=1)
                dpg.add_button(label="Reset")
                dpg.add_button(label="Step")
                dpg.add_checkbox(label="Run", default_value=False)

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