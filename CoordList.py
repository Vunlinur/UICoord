from os import linesep
from tkinter import Tk


class Coord:
    POINT = "POINT"
    RECTANGLE = "RECTANGLE"
    COLUMN_DEFAULTS = {
        "name": "Undefined",
        "x1": None,
        "y1": None,
        "x2": None,
        "y2": None,
    }

    def __init__(self, **kwargs):
        """
        Add variables to the object based on their static list.
        Set the variable to the value from kwargs, if given.
        Set to default otherwise.
        """
        [self.__setattr__(key, kwargs.get(key, val)) for key, val in self.COLUMN_DEFAULTS.items()]
        self.type = self.POINT if self.x2 == None and self.y2 == None else self.RECTANGLE

    def row_data(self):
        return [self.__getattribute__(key) or "" for key in self.COLUMN_DEFAULTS.keys()]


class CoordList(list):
    def __init__(self, widget: Tk):
        self.widget = widget
        self.display_coord = None
        self.get_pattern_callback = None
        super().__init__()

    def add_coord(self, coord):
        assert type(coord) == Coord
        self.append(coord)
        self.display_coord(coord.row_data())

    def get_coord(self, index):
        return self[index]

    def format_and_copy(self):
        rows = linesep.join([self.get_pattern_callback().format(**coord.__dict__) for coord in self])
        self.widget.clipboard_clear()
        self.widget.clipboard_append(rows)
