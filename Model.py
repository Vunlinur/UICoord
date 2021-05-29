import pickle
from io import BytesIO

from PIL.Image import Image, open as OpenImage

from Coord import Coord


class Model:
    class Serialized:
        def __init__(self):
            self.coords: list = None
            self.image = None

    def __init__(self):
        self._coords: dict = {}
        self._image_original: Image = None

    # Coords

    def get_coord(self, key: str):
        return self._coords[key]

    def set_coord(self, key: str, coord: Coord):
        self._coords[key] = coord

    def delete_coord(self, key: str):
        del self._coords[key]

    def get_coords(self):
        return self._coords

    def existing_names(self):
        return [coord.name for coord in self._coords.values()]

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
