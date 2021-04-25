from tkinter import *
from tkinter import ttk


class Menu(Frame):
    def __init__(self, parent: Tk, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        #  Member variables
        self.columns = ('Name', 'x', 'y', 'x2', 'y2')
        self.last_focus = None
        self.coord_text = StringVar()

        #  Setup UI
        self.menu = Frame(self.parent, width=400)
        self.menu.pack(side=LEFT, fill=Y, expand=False)
        self.menu.pack_propagate(0)

        self.label = Label(self.menu, textvariable=self.coord_text, font=18)
        self.label.pack()


        self.tree = ttk.Treeview(columns=self.columns, show='headings')
        scrollbar_y = ttk.Scrollbar(orient=VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(orient=HORIZONTAL, command=self.tree.xview)
        self.tree['yscroll'] = scrollbar_y.set
        self.tree['xscroll'] = scrollbar_x.set

        # add tree and scrollbars to frame
        self.coords = Frame(self.menu)
        self.tree.grid(in_=self.coords, row=0, column=0, sticky=NSEW)
        scrollbar_y.grid(in_=self.coords, row=0, column=1, sticky=NS)
        scrollbar_x.grid(in_=self.coords, row=1, column=0, sticky=EW)

        self.coords.grid_rowconfigure(0, weight=1)
        self.coords.grid_columnconfigure(0, weight=1)
        self.coords.pack(side=BOTTOM, fill=Y, expand=YES, padx=12, pady=12)

        for column in self.columns:
            self.tree.heading(column, text=column)
            width = 160 if column == "Name" else 60
            self.tree.column(column, minwidth=32, width=width, stretch=NO)

        # Binds, callbacks
        self.tree.bind("<Motion>", self.on_list_mouseover)
        self.tree.bind('<Button-1>', self.select_item)

        self.paint_marker_from_list_callback = None

    def on_list_mouseover(self, event):
        item_id = self.tree.identify_row(event.y)

        if item_id != self.last_focus:
            if self.last_focus:
                self.tree.item(self.last_focus, tags=[])

            self.tree.item(item_id, tags=["focus"])
            values = self.tree.item(item_id)['values']
            self.last_focus = item_id

            self.paint_marker_from_list_callback(values)

    def select_item(self, event):
        curItem = self.tree.focus()
        print(self.tree.item(curItem))

    def update_coords_label(self, x, y):
        self.coord_text.set('x:{:.4f}, y:{:.4f}'.format(x, y))

    def insert(self, item):
        self.tree.insert('', 'end', values=item)
