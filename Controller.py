from os import getcwd, linesep
from tkinter import *
from tkinter import filedialog, messagebox

from PIL import Image, ImageGrab, UnidentifiedImageError

from MenuView import MenuView
from Model import Coord, Model
from WorkspaceView import WorkspaceView


class Controller:
    supported_file_types = ".apng .blp .bmp .cur .eps .gif .icb .j2c .j2k .jp2 .jpc .jpe .jpeg .jpf .jpg .jps .jpx " \
                           ".mpo .pcx .pixar .png .pns .psd .pxr .tga .tif .tiff .vda .vst .xbm"
    project_extension = ".coord"
    project_file_types = [('Coord project files', project_extension)]

    def __init__(self, parent: Tk):
        self.parent = parent

        self.model = Model()
        self.menu = MenuView(self.parent)
        self.workspace = WorkspaceView(self.parent)

        # Setup Menu Bar
        self.menu_bar = Menu(self.parent)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New project", command=self.new_project_dialog, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open project", command=self.deserialize_dialog)
        self.file_menu.add_command(label="Save project", command=self.serialize_session, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save project as", command=self.serialize_dialog)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Open image", command=self.open_image_from_dialog)
        self.file_menu.add_command(label="Load image from clipboard", command=self.load_image_from_clipboard, accelerator="Ctrl+V")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Generate text output", command=self.format_and_copy)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Settings", command=..., state="disabled")
        self.menu_bar.add_cascade(label="Settings", menu=self.help_menu)

        self.parent.config(menu=self.menu_bar)

        # Project
        self.session = None

        self.new_project()

        # Callbacks
        self.workspace.add_coord_callback = self.add_coord
        self.workspace.get_coord_callback = self.get_coord
        self.workspace.update_coords_label_callback = self.menu.update_coords_label
        self.workspace.get_image_original_callback = self.model.get_image

        self.menu.paint_marker_from_list_callback = self.workspace.paint_marker_from_list
        self.menu.delete_coord_callback = self.model.delete_coord

        self.parent.bind('<Control-s>', lambda _: self.serialize_session())
        self.parent.bind('<Control-n>', lambda _: self.new_project_dialog())
        self.parent.bind('<Control-v>', lambda _: self.load_image_from_clipboard())

    # Coord

    def add_coord(self, coord: Coord):
        iid = self.menu.insert(coord.row_data())
        self.model.add_coord(iid, coord)

    def get_coord(self, index: str):
        return self.model.get_coord(index)

    def format_and_copy(self):
        rows = linesep.join(
            [self.menu.pattern.get().format(**coord.__dict__) for coord in self.model.get_coords().values()])
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
            ('image files', self.supported_file_types),
            ('all files', '.*')
        ]
        path = filedialog.askopenfilename(parent=self.parent,
                                          initialdir=getcwd(),
                                          title="Please select a file:",
                                          filetypes=file_types)
        if path:
            self.load_image_from_file(path)

    # Project

    def new_project(self):
        self.session = None
        image = Image.new('RGBA', (1, 1))
        self.model.__init__()
        self.model.set_image(image)
        self.workspace.load_image(image)
        self.menu.clear()

    def new_project_dialog(self):
        answer = messagebox.askokcancel("Create a new project", "Do you want to create a new project?")
        if answer:
            self.new_project()

    # Serialization

    def serialize_path(self, path):
        if not path.endswith(self.project_extension):
            path += self.project_extension
        self.model.serialize(path)
        self.session = path

    def serialize_session(self):
        if self.session:
            self.serialize_path(self.session)
        else:
            self.serialize_dialog()

    def serialize_dialog(self):
        path = filedialog.asksaveasfilename(parent=self.parent,
                                            initialdir=getcwd(),
                                            title="Please select a file name for saving:",
                                            filetypes=self.project_file_types)
        if path:
            self.serialize_path(path)

    def deserialize_path(self, path):
        self.session = path
        data = self.model.deserialize(path)
        self.menu.clear()
        for coord in data.coords:
            self.add_coord(coord)

        self.workspace.load_image(self.model.get_image())

    def deserialize_dialog(self):
        path = filedialog.askopenfilename(parent=self.parent,
                                          initialdir=getcwd(),
                                          title="Please select a project file to open:",
                                          filetypes=self.project_file_types)
        if path:
            self.deserialize_path(path)
