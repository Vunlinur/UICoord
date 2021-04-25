from cmath import sqrt
from tkinter import *
from tkinter import simpledialog

from PIL import ImageTk, Image


class Workspace(Frame):
    def __init__(self, parent: Tk, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        #  Setup UI
        self.canvas = Canvas(self.parent, bd=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES, padx=12, pady=12)

        #  Member variables
        self.image_original = Image.open("uisample.png")
        self.image = self.image_original
        self.photo_image = None  # set in on_resize
        self.image_aspect_ratio = self.image.size[0] / self.image.size[1]
        self.last_coord = (0.0, 0.0)
        self.marker = self.canvas.create_rectangle(0, 0, 0, 0)

        # Binds, callbacks
        self.canvas.bind('<Motion>', self.on_mouseover)
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_click_release)

        self.menu_insert_callback = None
        self.update_coords_label_callback = None

    def on_mouseover(self, event):
        self.update_coords_label_callback(
            event.x / self.image.size[0],
            event.y / self.image.size[1]
        )
        self.paint_marker_from_workspace(event)

    def paint_marker_from_workspace(self, event):
        if self.last_coord != (0, 0):
            self.clear_marker()
            self.marker = self.canvas.create_rectangle(self.last_coord[0], self.last_coord[1], event.x,
                                                       event.y, outline="red", width=2)

    def on_resize(self, event):
        self.clear_marker()
        workspace_aspect_ratio = event.width / event.height
        if self.image_aspect_ratio < workspace_aspect_ratio:
            scale = (int(event.height * self.image_aspect_ratio), event.height)
        else:
            scale = (event.width, int(event.width / self.image_aspect_ratio))
        self.image = self.image_original.resize(scale)
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)

    def on_click(self, event):
        self.last_coord = (event.x, event.y)

    def on_right_click(self, event):
        self.clear_marker()
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

        self.menu_insert_callback(coord)
        self.clear_marker()
        self.last_coord = (0, 0)

    def paint_marker_from_list(self, values):
        self.clear_marker()
        if type(values) == str:
            return

        kwargs = {
            "outline": "red",
            "width": 2
        }
        coords = values[1:]
        if len(coords) == 4:
            self.marker = self.canvas.create_rectangle(
                float(coords[0]) * self.image.size[0],
                float(coords[1]) * self.image.size[1],
                float(coords[2]) * self.image.size[0],
                float(coords[3]) * self.image.size[1],
                kwargs
            )
        else:
            radius = 3
            self.marker = self.canvas.create_oval(
                float(coords[0]) * self.image.size[0] - radius,
                float(coords[1]) * self.image.size[1] - radius,
                float(coords[0]) * self.image.size[0] + radius,
                float(coords[1]) * self.image.size[1] + radius,
                kwargs, fill="red"
            )

    def clear_marker(self):
        self.canvas.delete(self.marker)
