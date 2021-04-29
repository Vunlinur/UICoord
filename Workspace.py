from cmath import sqrt
from os import getcwd
from tkinter import *
from tkinter import simpledialog, filedialog, messagebox

from PIL import ImageTk, Image, ImageGrab

from CoordList import Coord


class Workspace(Canvas):
    supported_filetypes = ".apng .blp .bmp .cur .eps .gif .icb .j2c .j2k .jp2 .jpc .jpe .jpeg .jpf .jpg .jps .jpx " \
                          ".mpo .pcx .pixar .png .pns .psd .pxr .tga .tif .tiff .vda .vst .xbm"

    def __init__(self, parent: Tk, *args, **kwargs):
        Canvas.__init__(self, parent, bd=0, *args, **kwargs)
        self.parent = parent

        #  Setup UI
        self.pack(side=LEFT, fill=BOTH, expand=YES, padx=12, pady=12)

        #  Member variables
        self.image_original = None
        self.image = None
        self.photo_image = None
        self.image_aspect_ratio = 1.0
        self.scale = 1.0
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

    def load_image_from_clipboard(self):
        try:
            self.load_image(ImageGrab.grabclipboard())
        except AttributeError:
            messagebox.showinfo(message="Clipboard is Empty.")

    def load_image_from_file(self, path):
        self.load_image(Image.open(path))

    def load_image(self, image):
        self.image_original = image
        self.image_aspect_ratio = self.image_original.size[0] / self.image_original.size[1]
        # Gently calls on_resize function to fit the picture to the workspace.
        # Calling on_resize manually here executes it before the workspace is created and fails with its width/height.
        self.event_generate("<Configure>")

    def open_image_from_dialog(self):
        file_types = [
            ('image files', self.supported_filetypes),
            ('all files', '.*')
        ]
        path = filedialog.askopenfilename(parent=self,
                                          initialdir=getcwd(),
                                          title="Please select a file:",
                                          filetypes=file_types)
        self.load_image_from_file(path)

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
        self.winfo_width()
        width = self.winfo_width()
        height = self.winfo_height()
        workspace_aspect_ratio = width / height

        if self.image_aspect_ratio < workspace_aspect_ratio:
            scale = (int(height * self.image_aspect_ratio), height)
        else:
            scale = (width, int(width / self.image_aspect_ratio))

        if scale == self.scale:
            return
        else:
            self.scale = scale

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
