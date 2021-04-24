from cmath import sqrt
from tkinter import *
from tkinter import ttk, simpledialog

from PIL import ImageTk, Image


class MainApplication(Frame):
    def __init__(self, parent: Tk, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.geometry('1600x800')

        self.setup_menu()
        self.setup_workspace()

    def setup_menu(self):
        self.menu = Frame(self.parent, width=400)
        self.menu.pack(side=LEFT, fill=Y, expand=False)
        self.menu.pack_propagate(0)

        self.text = StringVar()
        self.label = Label(self.menu, textvariable=self.text, font=18)
        self.label.pack()

        self.coords = Frame(self.menu)

        self.columns = ('Name', 'x', 'y', 'x2', 'y2')
        self.tree = ttk.Treeview(columns=self.columns, show='headings')
        scrollbar_y = ttk.Scrollbar(orient=VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(orient=HORIZONTAL, command=self.tree.xview)
        self.tree['yscroll'] = scrollbar_y.set
        self.tree['xscroll'] = scrollbar_x.set

        # add tree and scrollbars to frame
        self.tree.grid(in_=self.coords, row=0, column=0, sticky=NSEW)
        scrollbar_y.grid(in_=self.coords, row=0, column=1, sticky=NS)
        scrollbar_x.grid(in_=self.coords, row=1, column=0, sticky=EW)

        for column in self.columns:
            self.tree.heading(column, text=column)
            width = 160 if column == "Name" else 60
            self.tree.column(column, minwidth=32, width=width, stretch=NO)

        self.coords.grid_rowconfigure(0, weight=1)
        self.coords.grid_columnconfigure(0, weight=1)
        self.coords.pack(side=BOTTOM, fill=Y, expand=YES, padx=12, pady=12)

    def setup_workspace(self):
        self.canvas = Canvas(self.parent, bd=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES, padx=12, pady=12)

        self.image_original = Image.open("uisample.png")
        self.image = self.image_original
        self.image_aspect_ratio = self.image.size[0] / self.image.size[1]
        self.last_coord = (0.0, 0.0)
        self.marker = self.canvas.create_rectangle(0, 0, 0, 0)
        self.last_focus = None

        self.canvas.bind('<Motion>', self.on_canvas_mouseover)
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_click_release)
        self.tree.bind("<Motion>", self.on_list_mouseover)
        self.tree.bind('<Button-1>', self.select_item)

    def on_canvas_mouseover(self, event):
        self.text.set('x:{:.4f}, y:{:.4f}'.format(
            event.x / self.image.size[0],
            event.y / self.image.size[1])
        )

        if self.last_coord != (0, 0):
            self.canvas.delete(self.marker)
            self.marker = self.canvas.create_rectangle(self.last_coord[0], self.last_coord[1], event.x, event.y,
                                                       outline="red", width=2)

    def on_resize(self, event):
        self.canvas.delete(self.marker)
        workspace_aspect_ratio = event.width / event.height
        if self.image_aspect_ratio < workspace_aspect_ratio:
            scale = (int(event.height * self.image_aspect_ratio), event.height)
        else:
            scale = (event.width, int(event.width / self.image_aspect_ratio))
        self.image = self.image_original.resize(scale)
        self.img = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.img)

    def on_click(self, event):
        self.last_coord = (event.x, event.y)

    def on_right_click(self, event):
        self.canvas.delete(self.marker)
        self.last_coord = (0, 0)

    def on_click_release(self, event):
        """
        Add the coordinates to the menu.tree list and delete the selection rectangle
        """
        if self.last_coord == (0, 0):
            # return when operation was cancelled by right-click
            return

        name = simpledialog.askstring("Name", "Enter the name of the coord:", parent=self.parent) or "Unnamed"
        distance = sqrt(
            pow(self.last_coord[0] - event.x, 2)
            + pow(self.last_coord[1] - event.y, 2)
        ).real
        if distance < 8:
            coord = (name,
                     event.x / self.image.size[0],
                     event.y / self.image.size[1])
        else:
            coord = (name,
                     self.last_coord[0] / self.image.size[0],
                     self.last_coord[1] / self.image.size[1],
                     event.x / self.image.size[0],
                     event.y / self.image.size[1])

        self.tree.insert('', 'end', values=coord)
        self.canvas.delete(self.marker)
        self.last_coord = (0, 0)

    def on_list_mouseover(self, event):
        item_id = self.tree.identify_row(event.y)

        if item_id != self.last_focus:
            if self.last_focus:
                self.tree.item(self.last_focus, tags=[])
            item = self.tree.item(item_id)
            self.last_focus = item_id
            self.canvas.delete(self.marker)

            if type(item['values']) == str:
                return

            coords = item["values"][1:]
            if len(coords) == 4:
                self.marker = self.canvas.create_rectangle(
                    float(coords[0]) * self.image.size[0],
                    float(coords[1]) * self.image.size[1],
                    float(coords[2]) * self.image.size[0],
                    float(coords[3]) * self.image.size[1],
                    outline="green", width=2)
            else:
                radius = 3
                self.marker = self.canvas.create_oval(
                    float(coords[0]) * self.image.size[0] - radius,
                    float(coords[1]) * self.image.size[1] - radius,
                    float(coords[0]) * self.image.size[0] + radius,
                    float(coords[1]) * self.image.size[1] + radius,
                    outline="red", width=2, fill="red")

    def select_item(self, event):
        curItem = self.tree.focus()
        print(self.tree.item(curItem))


if __name__ == "__main__":
    root = Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
