from tkinter import *
from tkinter.messagebox import showerror
from tkinter.ttk import Treeview

from Coord import Coord


class CoordEditFactory:
    def __init__(self, parent: Treeview):
        self._parent = parent
        self._edit_widget = None
        self.get_coord_callback = None
        self.set_coord_callback = None

    def close_widget(self):
        if self._edit_widget:
            self._edit_widget.destroy()

    def edit(self, row, column):
        self.close_widget()

        try:
            self._edit_widget = CoordEditWidget(
                self._parent,
                self.get_coord_callback,
                self.set_coord_callback,
                row,
                column
            )

            x, y, width, height = self._parent.bbox(row, column)
            self._edit_widget.place(x=x, y=y, anchor=NW, width=width)
        except TclError:  # Thrown when empty field is edited
            pass

        return self._edit_widget


class CoordEditWidget(Entry):
    def __init__(self, parent, get_coord_callback, set_coord_callback, row, column, **kw):
        super().__init__(parent, **kw)

        self._parent = parent
        self._set_coord_callback = set_coord_callback
        self._row = row
        self._column = column

        self._coord: Coord = get_coord_callback(row)
        self.insert(0, self._coord.column_data(self._column))
        self['exportselection'] = False  # Disables automatic copying selected text to clipboard

        self.bind("<Return>", self._on_return)
        self.bind("<Control-a>", lambda *_: self.select_all())
        self.bind("<Escape>", lambda *_: self.destroy())

        self.focus_force()

    def _on_return(self, event):
        text = self.get()
        if self._column in ("x1", "y1", "x2", "y2"):
            try:
                value = float(text)
            except ValueError:
                showerror("Error", "Entered value is not a float!")
                self.destroy()
                return

            if not 0 <= value <= 1:
                showerror("Error", "Entered value must be between 0 and 1 inclusive!")
                self.destroy()
                return
        else:
            value = text

        self._coord.column_data(self._column, value)
        self._set_coord_callback(self._row, self._coord)
        self.destroy()

    def select_all(self):
        self.selection_range(0, 'end')
        # returns 'break' to interrupt default key-bindings
        return 'break'
