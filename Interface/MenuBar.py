from os import getcwd
from tkinter import *
from tkinter import filedialog, messagebox

from Config import supported_image_file_types, project_file_types


class MenuBar(Menu):
    def __init__(self, parent: Tk, *args, **kwargs):
        Menu.__init__(self, parent, *args, **kwargs)

        self.get_session_callback = None
        self.load_image_from_file_callback = None
        self.new_project_callback = None
        self.serialize_path_callback = None
        self.deserialize_path_callback = None
        self.load_image_from_clipboard_callback = None
        self.load_image_from_adb_screenshot_callback = None
        self.export_menu_callback = None

        # Setup menu
        self.parent = parent
        self.file_menu = Menu(self, tearoff=0)
        self.file_menu.add_command(label="New project", command=self.new_project_dialog, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open project", command=self.deserialize_dialog)
        self.file_menu.add_command(label="Save project", command=self.serialize_session, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save project as", command=self.serialize_dialog)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Open image", command=self.open_image_from_dialog)
        self.file_menu.add_command(label="Load image from clipboard",
                                   command=lambda: self.load_image_from_clipboard_callback(),
                                   accelerator="Ctrl+V")
        self.file_menu.add_command(label="Capture screenshot via ADB",
                                   command=lambda: self.load_image_from_adb_screenshot_callback())
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Generate text output", command=lambda: self.export_menu_callback())
        self.add_cascade(label="File", menu=self.file_menu)

        self.help_menu = Menu(self, tearoff=0)
        self.help_menu.add_command(label="Settings", command=..., state="disabled")
        self.add_cascade(label="Settings", menu=self.help_menu)

        self.parent.config(menu=self)

        self.parent.bind('<Control-s>', lambda _: self.serialize_session())
        self.parent.bind('<Control-n>', lambda _: self.new_project_dialog())
        self.parent.bind('<Control-v>', lambda _: self.load_image_from_clipboard_callback())

    def open_image_from_dialog(self):
        file_types = [
            ('image files', supported_image_file_types),
            ('all files', '.*')
        ]
        path = filedialog.askopenfilename(parent=self.parent,
                                          initialdir=getcwd(),
                                          title="Please select a file:",
                                          filetypes=file_types)
        if path:
            self.load_image_from_file_callback(path)

    def new_project_dialog(self):
        answer = messagebox.askokcancel("Create a new project", "Do you want to create a new project?")
        if answer:
            self.new_project_callback()

    def serialize_session(self):
        session = self.get_session_callback()
        if session:
            self.serialize_path_callback(session)
        else:
            self.serialize_dialog()

    def serialize_dialog(self):
        path = filedialog.asksaveasfilename(parent=self.parent,
                                            initialdir=getcwd(),
                                            title="Please select a file name for saving:",
                                            filetypes=project_file_types)
        if path:
            self.serialize_path_callback(path)

    def deserialize_dialog(self):
        path = filedialog.askopenfilename(parent=self.parent,
                                          initialdir=getcwd(),
                                          title="Please select a project file to open:",
                                          filetypes=project_file_types)
        if path:
            self.deserialize_path_callback(path)
