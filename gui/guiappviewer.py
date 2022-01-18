import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "gui.ui"


class GuiAppViewer:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('windowViewer', master)
        
        self.FilterSendTxt = None
        self.FilterMsgFriend = None
        self.FilterMsgLocal = None
        self.FilterMsgNPC = None
        self.FilterMsgPlayer = None
        self.FilterMsgSquadron = None
        self.FilterMsgStarsystem = None
        self.FilterMsgVoicechat = None
        self.FilterMsgWing = None
        self.FilterFriendAdded = None
        self.FilterFriendDeclined = None
        self.FilterFriendLost = None
        self.FilterFriendOffline = None
        self.FilterFriendOnline = None
        self.FilterFriendRequested = None
        self.FilterDate = None
        self.FilterDateDays = None
        builder.import_variables(self, ['FilterSendTxt', 'FilterMsgFriend', 'FilterMsgLocal', 'FilterMsgNPC', 'FilterMsgPlayer', 'FilterMsgSquadron', 'FilterMsgStarsystem', 'FilterMsgVoicechat', 'FilterMsgWing', 'FilterFriendAdded', 'FilterFriendDeclined', 'FilterFriendLost', 'FilterFriendOffline', 'FilterFriendOnline', 'FilterFriendRequested', 'FilterDate', 'FilterDateDays'])
        
        builder.connect_callbacks(self)
    
    def run(self):
        self.mainwindow.mainloop()

    def buttonSelectDate(self):
        pass

    def buttonSaveTxt(self):
        pass

    def buttonRefresh(self):
        pass


if __name__ == '__main__':
    app = GuiAppViewer()
    app.run()


