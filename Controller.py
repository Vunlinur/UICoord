from argparse import ArgumentParser
from os import linesep
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageGrab, UnidentifiedImageError

from Config import project_extension
from Interface.MenuBar import MenuBar
from Interface.MenuView import MenuView
from Model import Coord, Model
from Interface.WorkspaceView import WorkspaceView


class Controller:
    def __init__(self, parent: Tk):
        self.parent = parent

        self.model = Model()
        self.menu = MenuView(self.parent)
        self.workspace = WorkspaceView(self.parent)
        self.menu_bar = MenuBar(self.parent)

        self.session = None

        # Callbacks
        self.menu_bar.get_session_callback = self.get_session
        self.menu_bar.load_image_from_file_callback = self.load_image_from_file
        self.menu_bar.new_project_callback = self.new_project
        self.menu_bar.serialize_path_callback = self.serialize_path
        self.menu_bar.deserialize_path_callback = self.deserialize_path
        self.menu_bar.load_image_from_clipboard_callback = self.load_image_from_clipboard
        self.menu_bar.format_and_copy_callback = self.format_and_copy

        self.workspace.add_coord_callback = self.add_coord
        self.workspace.get_coord_callback = self.get_coord
        self.workspace.update_coords_label_callback = self.menu.update_coords_label
        self.workspace.get_image_original_callback = self.model.get_image

        self.menu.paint_marker_from_list_callback = self.workspace.paint_marker_from_list
        self.menu.delete_coord_callback = self.model.delete_coord

        self.start()

    def start(self):
        """
        Parses command line arguments.
        Launches a new project if no arguments were specified.
        """
        parser = ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=False)
        group.add_argument('--open', '-o', type=str, )
        group.add_argument('--paste', '-p', action='store_true')
        args = parser.parse_args()

        if args.paste:
            self.load_image_from_clipboard()
            return

        if args.open:
            path = args.open
            if path.endswith(project_extension):
                self.deserialize_path(path)
            else:
                self.load_image_from_file(path)
            return

        self.new_project()

    def get_session(self):
        return self.session

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

    # Project

    def new_project(self):
        self.session = None
        image = Image.new('RGBA', (1, 1))
        self.model.__init__()
        self.model.set_image(image)
        self.workspace.load_image(image)
        self.menu.clear()

    # Serialization

    def serialize_path(self, path):
        if not path.endswith(project_extension):
            path += project_extension
        self.model.serialize(path)
        self.session = path

    def deserialize_path(self, path):
        self.session = path
        data = self.model.deserialize(path)
        self.menu.clear()
        for coord in data.coords:
            self.add_coord(coord)

        self.workspace.load_image(self.model.get_image())
