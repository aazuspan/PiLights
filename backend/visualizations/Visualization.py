import os
import sys


class Visualization:
    def __init__(self, pixels):
        self.pixels = pixels

    name = None
    description = None
    category = None
    hide = False

    def render(self):
        return

    @property
    def category(self):
        """
        Return the name of the folder that contains a given Visualization subclass
        """
        return str(os.path.split(os.path.dirname(sys.modules[self.__module__].__file__))[1])