from tkinter import *

from Controller import Controller


class MainApplication(Frame):
    def __init__(self, parent: Tk, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.geometry('1600x800')

        self.controller = Controller(self.parent)


if __name__ == "__main__":
    root = Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
