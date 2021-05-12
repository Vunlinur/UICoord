from tkinter import *
from tkinter import ttk

from Interface.CoordEditFactory import CoordEditFactory
from Model import Coord


class MenuView(Frame):
    def __init__(self, parent: Tk, *args, **kwargs):
        Frame.__init__(self, parent, width=400, *args, **kwargs)
        self.parent = parent

        #  Member variables
        self.columns = list(Coord.COLUMN_DEFAULTS.keys())
        self.last_hovered_coord = None  # Changes every time different widget is hovered over
        self.target_position = {'x': 0, 'y': 0}  # Points to the focused element, e.g. for editing
        self.coord_text = StringVar()
        self.pattern = StringVar()

        self.tree = ttk.Treeview(columns=self.columns, show='headings')
        self.coord_edit_factory = CoordEditFactory(self.tree)
        self.pattern.set('"{name}": ({x1}, {y1}, {x2}, {y2}),')
        self.update_coords_label(0, 0)

        #  Setup UI
        self.pack(side=LEFT, fill=Y, expand=False)
        self.pack_propagate(0)

        self.label = Label(self, textvariable=self.coord_text, font=18)
        self.label.pack()

        self.pattern_entry = Entry(self, textvariable=self.pattern)
        self.pattern_entry.pack(side=BOTTOM, fill=X, padx=12)

        #  Tree
        scrollbar_y = ttk.Scrollbar(orient=VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(orient=HORIZONTAL, command=self.tree.xview)
        self.tree['yscroll'] = scrollbar_y.set
        self.tree['xscroll'] = scrollbar_x.set

        for column in self.columns:
            self.tree.heading(column, text=column)
            width = 160 if column == "name" else 50
            self.tree.column(column, minwidth=32, width=width, stretch=NO)

        #  add tree and scrollbars to frame
        self.coords = Frame(self)
        self.tree.grid(in_=self.coords, row=0, column=0, sticky=NSEW)
        scrollbar_y.grid(in_=self.coords, row=0, column=1, sticky=NS)
        scrollbar_x.grid(in_=self.coords, row=1, column=0, sticky=EW)

        self.coords.grid_rowconfigure(0, weight=1)
        self.coords.grid_columnconfigure(0, weight=1)
        self.coords.pack(fill=Y, expand=YES, padx=12, pady=12)

        #  context menu
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.show_coord_edit_widget)
        self.context_menu.add_command(label="Delete", command=self.delete)
        self.context_menu.add_command(label="Select All", command=self.select_all)

        # Binds, callbacks
        self.tree.bind("<Motion>", self._on_list_mouseover)
        self.tree.bind("<Button-3>", self._on_right_click)
        self.tree.bind('<Double-1>', self._on_double_click)
        self.tree.bind("<Button>", lambda _: self.coord_edit_factory.close_widget())

        self.paint_marker_from_list_callback = None
        self.get_coord_callback = None
        self.set_coord_callback = None
        self.delete_coord_callback = None

    def configure_callbacks(self):
        self.coord_edit_factory.get_tree_callback = lambda: self.tree
        self.coord_edit_factory.get_coord_callback = self.get_coord_callback
        self.coord_edit_factory.set_coord_callback = self.set_coord_callback

    def _save_event_to_target_position(self, event: Event):
        self.target_position = {'x': event.x, 'y': event.y}

    def _on_list_mouseover(self, event):
        item_id = self.tree.identify_row(event.y)

        if item_id != self.last_hovered_coord:
            self.last_hovered_coord = item_id
            self.paint_marker_from_list_callback(item_id)

    def _on_right_click(self, event):
        self.coord_edit_factory.close_widget()
        self._save_event_to_target_position(event)

        item_id = self.tree.identify_row(event.y)
        if item_id:
            if item_id not in self.tree.selection():
                self.tree.selection_set(item_id)

            try:
                self.context_menu.post(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()

    def _on_double_click(self, event):
        self._save_event_to_target_position(event)
        self.show_coord_edit_widget()

    def update_coords_label(self, x, y):
        self.coord_text.set('x:{:.4f}, y:{:.4f}'.format(x, y))

    def show_coord_edit_widget(self):
        """
        Spawns a widget for editing the specific coord field under self.target_position
        """
        row = self.tree.identify_row(self.target_position['y'])
        if row:
            column = self.tree.identify_column(self.target_position['x'])
            # Col ID is needed to get attribute from a Coord object later
            column_id = self.tree.column(column)["id"]
            self.coord_edit_factory.edit(row, column_id)

    #  Treeview operations

    def insert_coord(self, item: Coord):
        return self.tree.insert('', 'end', values=item)

    def set_coord(self, key, values):
        self.tree.item(key, values=values)

    def delete(self):
        for index in self.tree.selection():
            self.delete_coord_callback(index)
            self.tree.delete(index)

    def select_all(self):
        self.tree.selection_set(self.tree.get_children())

    def clear(self):
        self.tree.delete(*self.tree.get_children())
