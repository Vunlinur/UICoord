from cmath import sqrt
from tkinter import *
from tkinter import simpledialog

from PIL import ImageTk, Image

from CoordList import Coord


class Workspace(Canvas):
    def __init__(self, parent: Tk, *args, **kwargs):
        Canvas.__init__(self, parent, bd=0, *args, **kwargs)
        self.parent = parent

        #  Setup UI
        self.pack(side=LEFT, fill=BOTH, expand=YES, padx=12, pady=12)

        #  Member variables
        self.image_original = Image.open("uisample.png")
        self.image = self.image_original
        self.photo_image = None  # set in on_resize
        self.image_aspect_ratio = self.image.size[0] / self.image.size[1]
        self.last_coord = (0.0, 0.0)
        self.marker = self.create_rectangle(0, 0, 0, 0)

        # Binds, callbacks
        self.bind('<Motion>', self.on_mouseover)
        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.on_click)
        self.bind("<Button-3>", self.on_right_click)
        self.bind("<ButtonRelease-1>", self.on_click_release)

        self.add_coord_callback = None
        self.get_coord_callback = None
        self.update_coords_label_callback = None

    def on_mouseover(self, event):
        self.update_coords_label_callback(
            event.x / self.image.size[0],
            event.y / self.image.size[1]
        )
        self.paint_marker_from_workspace(event)

    def paint_marker_from_workspace(self, event):
        if self.last_coord != (0, 0):
            self.delete(self.marker)
            self.marker = self.create_rectangle(self.last_coord[0], self.last_coord[1], event.x,
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
        self.create_image(0, 0, anchor=NW, image=self.photo_image)

    def on_click(self, event):
        self.last_coord = (event.x, event.y)

    def on_right_click(self, event):
        self.clear_marker()

    def on_click_release(self, event):
        """
        Add the coordinates to the menu.tree list and delete the selection rectangle
        """
        if self.last_coord == (0, 0):
            # return when operation was cancelled by right-click
            return

        name = simpledialog.askstring("Name", "Enter the name of the coord:", parent=self.parent)
        if name is None:
            self.clear_marker()
            return

        if name == "":
            name = name or "Unnamed"

        distance = sqrt(
            pow(self.last_coord[0] - event.x, 2)
            + pow(self.last_coord[1] - event.y, 2)
        ).real
        if distance < 8:
            coord = Coord(name=name,
                          x1=event.x / self.image.size[0],
                          y1=event.y / self.image.size[1]
            )
        else:
            coord = Coord(name=name,
                          x1=self.last_coord[0] / self.image.size[0],
                          y1=self.last_coord[1] / self.image.size[1],
                          x2=event.x / self.image.size[0],
                          y2=event.y / self.image.size[1]
            )

        self.add_coord_callback(coord)
        self.clear_marker()

    def paint_marker_from_list(self, index):
        self.clear_marker()
        if index == -1:
            return

        kwargs = {
            "outline": "red",
            "width": 2
        }
        coord = self.get_coord_callback(index)
        if coord.type == coord.RECTANGLE:
            self.marker = self.create_rectangle(
                coord.x1 * self.image.size[0],
                coord.y1 * self.image.size[1],
                coord.x2 * self.image.size[0],
                coord.y2 * self.image.size[1],
                kwargs
            )
        else:
            radius = 3
            self.marker = self.create_oval(
                coord.x1 * self.image.size[0] - radius,
                coord.y1 * self.image.size[1] - radius,
                coord.x1 * self.image.size[0] + radius,
                coord.y1 * self.image.size[1] + radius,
                kwargs, fill="red"
            )

    def clear_marker(self):
        self.last_coord = (0, 0)
        self.delete(self.marker)
