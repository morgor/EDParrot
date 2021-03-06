import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "gui.ui"


class GuiApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('windowDateSelector', master)
        builder.connect_callbacks(self)
    
    def run(self):
        self.mainwindow.mainloop()

    def buttonSelectDate(self):
        pass


if __name__ == '__main__':
    app = GuiApp()
    app.run()


