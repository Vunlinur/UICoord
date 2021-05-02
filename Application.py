from tkinter import *

from Controller import Controller


class MainApplication(Frame):
    def __init__(self, parent: Tk, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.geometry('1600x800')

        self.controller = Controller(self.parent)
        self.controller.deserialize_path("kiru.coord")
        #self.controller.load_image_from_file("uisample.png")

        self.menu_bar = Menu(self.parent)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New project", command=..., state="disabled")
        self.file_menu.add_command(label="Open project", command=self.controller.deserialize)
        self.file_menu.add_command(label="Save project", command=self.controller.serialize)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Open image", command=self.controller.open_image_from_dialog)
        self.file_menu.add_command(label="Load image from clipboard", command=self.controller.load_image_from_clipboard)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Generate text output", command=self.controller.format_and_copy)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Settings", command=..., state="disabled")
        self.menu_bar.add_cascade(label="Settings", menu=self.help_menu)

        self.parent.config(menu=self.menu_bar)


if __name__ == "__main__":
    root = Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
