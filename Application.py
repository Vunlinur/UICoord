from tkinter import *

from CoordList import CoordList
from CoordMenu import CoordMenu as CoordMenu
from Workspace import Workspace


class MainApplication(Frame):
    def __init__(self, parent: Tk, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.geometry('1600x800')

        self.menu = CoordMenu(self.parent)
        self.workspace = Workspace(self.parent)
        self.coord_list_MVC = CoordList(self.parent)

        self.menu_bar = Menu(self.parent)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New project", command=..., state="disabled")
        self.file_menu.add_command(label="Open project", command=..., state="disabled")
        self.file_menu.add_command(label="Save project", command=..., state="disabled")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Open image", command=self.workspace.open_image_from_dialog)
        self.file_menu.add_command(label="Load image from clipboard", command=self.workspace.load_image_from_clipboard)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Generate text output", command=self.coord_list_MVC.format_and_copy)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Settings", command=..., state="disabled")
        self.menu_bar.add_cascade(label="Settings", menu=self.help_menu)

        self.parent.config(menu=self.menu_bar)

        self.workspace.load_image_from_file("uisample.png")

        # Callbacks
        self.workspace.add_coord_callback = self.coord_list_MVC.add_coord
        self.workspace.get_coord_callback = self.coord_list_MVC.get_coord
        self.workspace.update_coords_label_callback = self.menu.update_coords_label

        self.coord_list_MVC.display_coord = self.menu.insert
        self.coord_list_MVC.get_pattern_callback = self.menu.pattern.get

        self.menu.paint_marker_from_list_callback = self.workspace.paint_marker_from_list


if __name__ == "__main__":
    root = Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
