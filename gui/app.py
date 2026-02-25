import dearpygui.dearpygui as dpg
import engine as eng

#always first command
def main():
    dpg.create_context()
    with dpg.window(tag="Primary Window"):
        with dpg.group():
            dpg.add_text("Conway's Game of Life")
            dpg.add_text("Links: Board.\t Rechts: Einstellungen.")
            dpg.add_separator()

        with dpg.group(horizontal=True):
            # Links: Spielfeld-Container
            with dpg.child_window(width=300, height=200, border=True):
                values = (0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0,
                          2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0,
                          1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0,
                          0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0,
                          0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0,
                          1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1,
                          0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3)
                dpg.add_text("BOARD AREA")
                with dpg.plot(label="Board", no_mouse_pos=True, height=300, width=-1):
                    #dpg.add_plot_axis(dpg.mvXAxis, lock_min=True, lock_max=True, no_gridlines=False,
                    #                  no_tick_marks=False)
                    #with dpg.plot_axis(dpg.mvYAxis, label="y", no_gridlines=True, no_tick_marks=True, lock_min=True,
                    #                   lock_max=True):
                        dpg.add_heat_series(values, 7, 7, tag="heat_series")

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