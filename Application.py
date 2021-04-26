from tkinter import *

from CoordList import CoordList
from Menu import Menu as CoordMenu
from Workspace import Workspace


class MainApplication(Frame):
    def __init__(self, parent: Tk, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.geometry('1600x800')

        self.menu = CoordMenu(self.parent)
        self.workspace = Workspace(self.parent)
        self.coord_list_MVC = CoordList(self.parent)

        # Callbacks
        self.workspace.add_coord_callback = self.coord_list_MVC.add_coord
        self.workspace.get_coord_callback = self.coord_list_MVC.get_coord
        self.workspace.update_coords_label_callback = self.menu.update_coords_label

        self.coord_list_MVC.display_coord = self.menu.insert
        self.coord_list_MVC.get_pattern_callback = self.menu.pattern.get

        self.menu.paint_marker_from_list_callback = self.workspace.paint_marker_from_list
        self.menu.export_button.bind('<Button-1>', self.coord_list_MVC.format_and_copy)


if __name__ == "__main__":
    root = Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
