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

        # context menu
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Delete", command=self.delete)
        self.context_menu.add_command(label="Select All", command=self.select_all)

        # export
        self.export = Frame(self)
        self.export.pack(side=BOTTOM, fill=X, padx=12, pady=12)

        self.pattern_entry = Entry(self.export, textvariable=self.pattern)
        self.pattern_entry.pack(side=LEFT, fill=X, expand=Y)

        # Binds, callbacks
        self.tree.bind("<Motion>", self.on_list_mouseover)
        self.tree.bind("<Button-3>", self.on_right_click)

        self.paint_marker_from_list_callback = None
        self.delete_coord_callback = None

    def on_list_mouseover(self, event):
        item_id = self.tree.identify_row(event.y)

        if item_id != self.last_focus:
            self.last_focus = item_id
            self.paint_marker_from_list_callback(item_id)

    def on_right_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id:
            if item_id not in self.tree.selection():
                self.tree.selection_set(item_id)

            try:
                self.context_menu.post(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()

    def update_coords_label(self, x, y):
        self.coord_text.set('x:{:.4f}, y:{:.4f}'.format(x, y))

    def insert(self, item: Coord):
        return self.tree.insert('', 'end', values=item)

    def delete(self):
        for index in self.tree.selection():
            self.delete_coord_callback(index)
            self.tree.delete(index)

    def select_all(self):
        self.tree.selection_set(self.tree.get_children())

    def clear(self):
        self.tree.delete(*self.tree.get_children())
