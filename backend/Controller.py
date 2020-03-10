import importlib
import pkgutil

from backend import constants
from backend.visualizations.Visualization import Visualization


class Controller:
    def get_visualizations(self):
        """
        Get all subclasses of Visualization in the visualizations directory
        :return: A list of all Visualization subclasses
        """
        for (module_loader, name, ispkg) in pkgutil.iter_modules([constants.VIS_DIR]):
            importlib.import_module('backend.visualizations.' + name, __package__)

        return Visualization.__subclasses__()
