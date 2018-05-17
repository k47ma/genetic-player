from shapes import *

class Chart:
    def __init__(self, x_values=None, y_values=None, x_resolution=None, y_resolution=None,
                 constants=None, caption=None, width=100, height=60, pos=(0, 0)):
        self.x_values = x_values
        self.y_values = y_values
        self.x_resolution = x_resolution
        self.y_resolution = y_resolution
        self.constants = constants
        self.caption = caption
        self.width = width
        self.height = height
        self.offset = pos

        self.x_range = None
        self.y_range = None

        self._setup()

    def _setup(self):
        # calculate the range for x and y
        if self.x_values:
            self.x_range = (min(self.x_values), max(self.x_values))
        if self.y_values:
            self.y_range = (min(self.y_values), max(self.y_values))

        # calculate the resolution for x and y
        if not self.x_resolution:
            self.x_resolution = (self.x_range[1] - self.x_range[0]) / 10.0
        if not self.y_resolution:
            self.y_resolution = (self.y_range[1] - self.y_range[0]) / 10.0

    def get_shapes(self):
        """returns a list of shapes for plotting"""
        return []
