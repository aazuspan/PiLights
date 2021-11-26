import os
import sys

class VisualizationMeta(type):
    """This metaclass allows a repr for classes rather than instances"""
    def __repr__(cls):
        return cls.name

class Visualization(metaclass=VisualizationMeta):
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