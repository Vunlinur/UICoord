import pickle
from io import BytesIO

from PIL.Image import Image, open as OpenImage


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
    class Serialized:
        def __init__(self):
            self.coords: list = None
            self.image = None

    def __init__(self):
        self._coords: dict = {}
        self._image_original: Image = None

    # Coords

    def add_coord(self, key: str, coord: Coord):
        self._coords[key] = coord

    def delete_coord(self, key: str):
        del self._coords[key]

    def get_coord(self, key: str):
        return self._coords[key]

    def get_coords(self):
        return self._coords

    # Image

    def set_image(self, image: Image):
        self._image_original = image

    def get_image(self) -> Image:
        return self._image_original

    # Serialization

    def serialize(self, path):
        #  Because PIL.Image.tobytes() is broken:
        #  https://stackoverflow.com/questions/31077366/pil-cannot-identify-image-file-for-io-bytesio-object
        byteImgIO = BytesIO()
        self._image_original.save(byteImgIO, "PNG")
        byteImgIO.seek(0)

        data = self.Serialized()
        # We need to ensure we do not duplicate keys upon deserializing, so we can discard them
        data.coords = list(self._coords.values())
        data.image = byteImgIO.read()

        pickle.dump(data, open(path, "wb"))

    def deserialize(self, path):
        self.__init__()

        data: Model.Serialized = pickle.load(open(path, "rb"))
        self._image_original = OpenImage(BytesIO(data.image))
        # We have to return the coords as they have to be added to the UI first.
        # This is where we get the Model dict key from.
        return data
