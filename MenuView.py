from tkinter import *
from tkinter import ttk

from Model import Coord


class MenuView(Frame):
    def __init__(self, parent: Tk, *args, **kwargs):
        Frame.__init__(self, parent, width=400, *args, **kwargs)
        self.parent = parent

        #  Member variables
        self.columns = list(Coord.COLUMN_DEFAULTS.keys())
        self.last_focus = None
        self.coord_text = StringVar()
        self.update_coords_label(0, 0)
        self.pattern = StringVar()
        self.pattern.set('"{name}": ({x1}, {y1}, {x2}, {y2}),')

        #  Setup UI
        self.pack(side=LEFT, fill=Y, expand=False)
        self.pack_propagate(0)

        self.label = Label(self, textvariable=self.coord_text, font=18)
        self.label.pack()

        # tree
        self.tree = ttk.Treeview(columns=self.columns, show='headings')
        scrollbar_y = ttk.Scrollbar(orient=VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(orient=HORIZONTAL, command=self.tree.xview)
        self.tree['yscroll'] = scrollbar_y.set
        self.tree['xscroll'] = scrollbar_x.set

        for column in self.columns:
            self.tree.heading(column, text=column)
            width = 160 if column == "name" else 60
            self.tree.column(column, minwidth=32, width=width, stretch=NO)

        # add tree and scrollbars to frame
        self.coords = Frame(self)
        self.tree.grid(in_=self.coords, row=0, column=0, sticky=NSEW)
        scrollbar_y.grid(in_=self.coords, row=0, column=1, sticky=NS)
        scrollbar_x.grid(in_=self.coords, row=1, column=0, sticky=EW)

        self.coords.grid_rowconfigure(0, weight=1)
        self.coords.grid_columnconfigure(0, weight=1)
        self.coords.pack(fill=Y, expand=YES, padx=12, pady=12)

        # export
        self.export = Frame(self)
        self.export.pack(side=BOTTOM, fill=X, padx=12, pady=12)

        self.pattern_entry = Entry(self.export, textvariable=self.pattern)
        self.pattern_entry.pack(side=LEFT, fill=X, expand=Y)

        # Binds, callbacks
        self.tree.bind("<Motion>", self.on_list_mouseover)

        self.paint_marker_from_list_callback = None

    def on_list_mouseover(self, event):
        item_id = self.tree.identify_row(event.y)

        if item_id != self.last_focus:
            if self.last_focus:
                self.tree.item(self.last_focus, tags=[])

            self.tree.item(item_id, tags=["focus"])

            index = int(item_id) - 1 if item_id != "" else -1
            self.paint_marker_from_list_callback(index)

    def update_coords_label(self, x, y):
        self.coord_text.set('x:{:.4f}, y:{:.4f}'.format(x, y))

    def insert(self, item):
        # Assigning to index 0 results in assigning to the default "I001".
        # The numeration does not reset when clearing the list, I deal with it with a custom index.
        index = len(self.tree.get_children()) + 1
        self.tree.insert('', 'end', index, values=item)

    def clear(self):
        self.tree.delete(*self.tree.get_children())
