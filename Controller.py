from os import getcwd, linesep
from tkinter import *
from tkinter import filedialog, messagebox

from PIL import Image, ImageGrab, UnidentifiedImageError

from MenuView import MenuView
from Model import Coord, Model
from WorkspaceView import WorkspaceView


class Controller:
    supported_filetypes = ".apng .blp .bmp .cur .eps .gif .icb .j2c .j2k .jp2 .jpc .jpe .jpeg .jpf .jpg .jps .jpx " \
                          ".mpo .pcx .pixar .png .pns .psd .pxr .tga .tif .tiff .vda .vst .xbm"

    def __init__(self, parent: Tk):
        self.parent = parent

        self.model = Model()
        self.menu = MenuView(self.parent)
        self.workspace = WorkspaceView(self.parent)

        # Callbacks
        self.workspace.add_coord_callback = self.add_coord
        self.workspace.get_coord_callback = self.get_coord
        self.workspace.update_coords_label_callback = self.menu.update_coords_label
        self.workspace.get_image_original_callback = self.model.get_image

        self.menu.paint_marker_from_list_callback = self.workspace.paint_marker_from_list

    # Coord

    def add_coord(self, coord: Coord):
        self.model.add_coord(coord)
        self.menu.insert(coord.row_data())

    def get_coord(self, index: int):
        return self.model.get_coord(index)

    def format_and_copy(self):
        rows = linesep.join(
            [self.menu.pattern.get().format(**coord.__dict__) for coord in self.model.get_coord_list()])
        self.parent.clipboard_clear()
        self.parent.clipboard_append(rows)

    # Image

    def load_image_from_clipboard(self):
        try:
            image = ImageGrab.grabclipboard()
            self.model.set_image(image)
            self.workspace.load_image(image)
        except AttributeError:
            messagebox.showinfo(message="Clipboard is Empty.")

    def load_image_from_file(self, path):
        try:
            image = Image.open(path)
            self.model.set_image(image)
            self.workspace.load_image(image)
        except UnidentifiedImageError:
            messagebox.showinfo(message="Invalid image file.")

    def open_image_from_dialog(self):
        file_types = [
            ('image files', self.supported_filetypes),
            ('all files', '.*')
        ]
        path = filedialog.askopenfilename(parent=self.parent,
                                          initialdir=getcwd(),
                                          title="Please select a file:",
                                          filetypes=file_types)
        if path:
            self.load_image_from_file(path)
