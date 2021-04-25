from tkinter import *

from Menu import Menu as CoordMenu
from Workspace import Workspace


class MainApplication(Frame):
    def __init__(self, parent: Tk, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.geometry('1600x800')

        self.menu = CoordMenu(self.parent)
        self.workspace = Workspace(self.parent)

        self.workspace.menu_insert_callback = self.menu.insert
        self.workspace.update_coords_label_callback = self.menu.update_coords_label
        self.menu.paint_marker_from_list_callback = self.workspace.paint_marker_from_list


if __name__ == "__main__":
    root = Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
