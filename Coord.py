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