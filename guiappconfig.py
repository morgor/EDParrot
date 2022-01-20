import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "gui.ui"


class GuiAppConfig:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('windowConfig', master)
        
        self.__tkvar = None
        self.TrFriend = None
        self.TrLocal = None
        self.TrNPC = None
        self.TrPlayer = None
        self.TrSquadron = None
        self.TrStarsystem = None
        self.TrVoicechat = None
        self.TrWing = None
        self.TrFrAdd = None
        self.TrFrDecline = None
        self.TrFrLost = None
        self.TrFrOffiline = None
        self.TrFrOnline = None
        self.TrFrRequest = None
        self.PrintMsg = None
        self.AOTop = None
        builder.import_variables(self, ['__tkvar', 'TrFriend', 'TrLocal', 'TrNPC', 'TrPlayer', 'TrSquadron', 'TrStarsystem', 'TrVoicechat', 'TrWing', 'TrFrAdd', 'TrFrDecline', 'TrFrLost', 'TrFrOffiline', 'TrFrOnline', 'TrFrRequest', 'PrintMsg', 'AOTop'])
        
        builder.connect_callbacks(self)
    
    def run(self):
        self.mainwindow.mainloop()

    def buttonLoadConfig(self):
        pass

    def buttonSaveConfig(self):
        pass

    def buttonLoadDefaultConfig(self):
        pass

    def buttonSaveDefaultConfig(self):
        pass


if __name__ == '__main__':
    app = GuiAppConfig()
    app.run()


