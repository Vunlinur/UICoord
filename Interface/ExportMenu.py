from _csv import reader
from os import linesep
from tkinter import *
from tkinter.ttk import Combobox

from Model import Coord


class ExportMenu(Toplevel):
    color_error = '#ff9898'
    sample_dict = {"name": "test",
                   "x1": 0.123456789012345678901234567890,
                   "x2": 0.234567890123456789012345678901,
                   "y1": 0.345678901234567890123456789012,
                   "y2": 0.456789012345678901234567890123}

    class Config:
        def __init__(self, entry_output, sample_output, pattern):
            self.entry_output = entry_output
            self.sample_output = sample_output
            self.pattern = pattern

    def __init__(self, parent: Tk, *args, **kwargs):
        Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.resizable(1, 0)
        self.grab_set()
        self.geometry('600x230')

        #  Member variables
        self.preset_pattern = StringVar()
        self.point_pattern = StringVar()
        self.rect_pattern = StringVar()
        self.sample_output_rect = StringVar()
        self.sample_output_point = StringVar()

        # Contains the types of sample outputs that are currently errored, enabling accurate button disabling
        self.error_set = set()

        with open('exportpresets.csv') as csv_file:
            csv_reader = reader(
                csv_file,
                delimiter='|',
                skipinitialspace=False,
                quotechar=None
            )
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
        self.label_output_point = Label(self, text="Sample output")
        self.label_output_point.grid(in_=self, row=2, column=0, sticky=E, padx=padx, pady=pady)
        self.label_rect = Label(self, text="Rectangle pattern")
        self.label_rect.grid(in_=self, row=3, column=0, sticky=E, padx=padx, pady=pady)
        self.label_output_rect = Label(self, text="Sample output")
        self.label_output_rect.grid(in_=self, row=4, column=0, sticky=E, padx=padx, pady=pady)

        self.preset_menu = Combobox(self, textvariable=self.preset_pattern, values=names)
        self.preset_menu.grid(in_=self, row=0, column=1, sticky=EW, padx=padx, pady=pady)
        self.entry_point = Entry(self, textvariable=self.point_pattern)
        self.entry_point.grid(in_=self, row=1, column=1, sticky=EW, padx=padx, pady=pady)
        self.entry_output_point = Entry(self, textvariable=self.sample_output_point)
        self.entry_output_point.grid(in_=self, row=2, column=1, sticky=EW, padx=padx, pady=pady)
        self.entry_rect = Entry(self, textvariable=self.rect_pattern)
        self.entry_rect.grid(in_=self, row=3, column=1, sticky=EW, padx=padx, pady=pady)
        self.entry_output_rect = Entry(self, textvariable=self.sample_output_rect)
        self.entry_output_rect.grid(in_=self, row=4, column=1, sticky=EW, padx=padx, pady=pady)

        self.reset_button = Button(self, text="Reset", command=self.set_patterns)
        self.reset_button.grid(in_=self, row=5, column=0, sticky=NS, padx=padx, pady=pady)
        self.export_button = Button(self, text="Export", command=self.export)
        self.export_button.grid(in_=self, row=5, column=1, sticky=NS, padx=padx, pady=pady)

        self.grid_columnconfigure(1, weight=1)

        self.config = {
            "point": self.Config(
                self.entry_output_point,
                self.sample_output_point,
                self.point_pattern
            ),
            "rect": self.Config(
                self.entry_output_rect,
                self.sample_output_rect,
                self.rect_pattern
            )
        }

        # Binds, callbacks
        self.preset_menu.bind("<<ComboboxSelected>>", lambda _: self.set_patterns())
        self.entry_output_point.bind("<Key>", lambda e: "break")
        self.entry_output_rect.bind("<Key>", lambda e: "break")
        self.point_pattern.trace("w", lambda name, index, mode, sv=self.rect_pattern: self.update_sample_output("point"))
        self.rect_pattern.trace("w", lambda name, index, mode, sv=self.rect_pattern: self.update_sample_output("rect"))

        self.get_coords_callback = None

        for key in self.config.keys():
            self.update_sample_output(key)

    def set_patterns(self):
        preset = self.preset_pattern.get()
        self.rect_pattern.set(self.export_presets[preset][0])  # 1st column of csv
        self.point_pattern.set(self.export_presets[preset][1])  # 2nd column of csv

    def update_sample_output(self, type: str):
        entry_output = self.config[type].entry_output
        sample_output = self.config[type].sample_output
        pattern = self.config[type].pattern

        entry_output.config(bg=self.parent.cget('bg'))
        try:
            sample_output.set(pattern.get().format(**self.sample_dict))
        except:
            entry_output.config(bg=self.color_error)
            self.error_set.add(type)
            self.export_button.config(state='disabled')
        else:
            if type in self.error_set:
                self.error_set.remove(type)
            if not self.error_set:
                self.export_button.config(state='normal')

    def export(self):
        rows = linesep.join(
            [(self.point_pattern if coord.type == Coord.POINT else self.rect_pattern)
                 .get()
                 .format(**coord.__dict__)
             for coord in self.get_coords_callback().values()]
        )
        self.parent.clipboard_clear()
        self.parent.clipboard_append(rows)
