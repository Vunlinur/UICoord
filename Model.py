import PIL

from PIL import Image


class Coord:
    POINT = "POINT"
    RECTANGLE = "RECTANGLE"
    COLUMN_DEFAULTS = {
        "name": "Undefined",
        "x1": None,
        "y1": None,
        "x2": None,
        "y2": None,
    }

    def __init__(self, **kwargs):
        """
        Add variables to the object based on their static list.
        Set the variable to the value from kwargs, if given.
        Set to default otherwise.
        """
        [self.__setattr__(key, kwargs.get(key, val)) for key, val in self.COLUMN_DEFAULTS.items()]
        self.type = self.POINT if self.x2 == None and self.y2 == None else self.RECTANGLE

    def row_data(self):
        return [self.__getattribute__(key) or "" for key in self.COLUMN_DEFAULTS.keys()]


class Model:
    def __init__(self):
        self._coord_list: list = []
        self._image_original: PIL.Image = None

    def add_coord(self, coord: Coord):
        self._coord_list.append(coord)

    def get_coord(self, index: int):
        return self._coord_list[index]

    def get_coord_list(self):
        return self._coord_list

    def set_image(self, image: PIL.Image):
        self._image_original = image

    def get_image(self):
        return self._image_original
