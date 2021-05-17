from _csv import reader
from os import linesep
from tkinter import *
from tkinter.ttk import Combobox

from Model import Coord


class ExportMenu(Toplevel):
    def __init__(self, parent: Tk, *args, **kwargs):
        Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.resizable(1, 0)
        self.grab_set()
        self.geometry('600x160')

        #  Member variables
        self.preset_pattern = StringVar()
        self.point_pattern = StringVar()
        self.rect_pattern = StringVar()

        with open('exportpresets.csv') as csv_file:
            csv_reader = reader(csv_file, delimiter='|')
            self.export_presets = {row[0]: row[1:] for row in csv_reader}

        names = list(self.export_presets.keys())
        self.preset_pattern.set(names[0])

        self.set_patterns()

        #  Setup UI
        padx = 12
        pady = 8

        self.label_preset = Label(self, text="Preset")
        self.label_preset.grid(in_=self, row=0, column=0, sticky=E, padx=padx, pady=pady)
        self.label_point = Label(self, text="Point pattern")
        self.label_point.grid(in_=self, row=1, column=0, sticky=E, padx=padx, pady=pady)
        self.label_rect = Label(self, text="Rectangle pattern")
        self.label_rect.grid(in_=self, row=2, column=0, sticky=E, padx=padx, pady=pady)

        self.preset_menu = Combobox(self, textvariable=self.preset_pattern, values=names)
        self.preset_menu.grid(in_=self, row=0, column=1, sticky=EW, padx=padx, pady=pady)
        self.entry_point = Entry(self, textvariable=self.point_pattern)
        self.entry_point.grid(in_=self, row=1, column=1, sticky=EW, padx=padx, pady=pady)
        self.entry_rect = Entry(self, textvariable=self.rect_pattern)
        self.entry_rect.grid(in_=self, row=2, column=1, sticky=EW, padx=padx, pady=pady)

        self.reset_button = Button(self, text="Reset", command=lambda _: self.set_patterns())
        self.reset_button.grid(in_=self, row=3, column=0, sticky=NS, padx=padx, pady=pady)
        self.export_button = Button(self, text="Export", command=self.export)
        self.export_button.grid(in_=self, row=3, column=1, sticky=NS, padx=padx, pady=pady)

        self.grid_columnconfigure(1, weight=1)

        # Binds, callbacks
        self.preset_menu.bind("<<ComboboxSelected>>", lambda _: self.set_patterns())

        self.get_coords_callback = None

    def set_patterns(self):
        preset = self.preset_pattern.get()
        self.rect_pattern.set(self.export_presets[preset][0])
        self.point_pattern.set(self.export_presets[preset][1])

    def export(self):
        rows = linesep.join(
            [(self.point_pattern if coord.type == Coord.POINT else self.rect_pattern)
                 .get()
                 .format(**coord.__dict__)
             for coord in self.get_coords_callback().values()]
        )
        self.parent.clipboard_clear()
        self.parent.clipboard_append(rows)
