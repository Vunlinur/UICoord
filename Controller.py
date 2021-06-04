from argparse import ArgumentParser
from os import system, remove
from threading import Thread
from tkinter import *
from tkinter.messagebox import showinfo

from PIL import Image, ImageGrab, UnidentifiedImageError

from Config import project_extension
from Interface.ExportMenu import ExportMenu
from Interface.MenuBar import MenuBar
from Interface.MenuView import MenuView
from Interface.WorkspaceView import WorkspaceView
from Model import Coord, Model


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
        self.menu_bar.load_image_from_adb_screenshot_callback = self.load_image_from_adb_screenshot
        self.menu_bar.export_menu_callback = self.toggle_export_menu

        self.workspace.add_coord_callback = self.add_coord
        self.workspace.get_coord_callback = self.get_coord
        self.workspace.update_coords_label_callback = self.menu.update_coords_label
        self.workspace.get_image_original_callback = self.model.get_image

        self.menu.clear_marker_callback = self.workspace.clear_marker
        self.menu.paint_marker_from_coord_callback = self.workspace.paint_marker_from_coord
        self.menu.get_coord_callback = self.get_coord
        self.menu.set_coord_callback = self.set_coord
        self.menu.delete_coord_callback = self.model.delete_coord

        self.menu.configure_callbacks()
        self.initialize()

    def initialize(self):
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
        if coord.name in self.model.existing_names():
            return False
        key = self.menu.insert_coord(coord)
        self.model.set_coord(key, coord)
        return True

    def get_coord(self, key: str):
        return self.model.get_coord(key)

    def set_coord(self, key: str, coord: Coord):
        if coord.name in self.model.existing_names():
            return False
        self.model.set_coord(key, coord)
        self.menu.set_coord(key, coord)
        return True

    def get_coords(self):
        return self.model.get_coords()

    def toggle_export_menu(self):
        self.export_menu = ExportMenu(self.parent)
        self.export_menu.get_coords_callback = self.get_coords

    # Image

    def load_image_from_clipboard(self):
        try:
            image = ImageGrab.grabclipboard()
            self.model.set_image(image)
            self.workspace.load_image(image)
        except AttributeError:
            showinfo(message="Clipboard is Empty.")

    def load_image_from_file(self, path):
        try:
            image = Image.open(path)
            self.model.set_image(image)
            self.workspace.load_image(image)
        except UnidentifiedImageError:
            showinfo(message="Invalid image file.")

    def load_image_from_adb_screenshot(self):
        def capture_and_open():
            temp_file = "temp_coord_screenshot.png"
            result = system("adb exec-out screencap -p > " + temp_file)
            if result != 0:
                showinfo(message="Error communicating with ADB. Please ensure it is added to PATH.")
                return
            self.load_image_from_file(temp_file)
            remove(temp_file)

        thread = Thread(target=capture_and_open)
        thread.start()

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
