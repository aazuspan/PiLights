import importlib
import pkgutil

from backend import constants
from backend.visualizations.Visualization import Visualization


class Controller:
    def get_visualizations(self, filter_category):
        """
        Get all subclasses of Visualization in the visualizations directory
        :param filter_category: str name of category to return visualizations for
        :return: A list of all Visualization subclasses
        """
        visualizations = None

        for (module_loader, name, ispkg) in pkgutil.iter_modules([constants.VIS_DIR]):
            importlib.import_module('backend.visualizations.' + name, __package__)

        if filter_category:
            visualizations = self.get_visualizations_by_category(visualizations=Visualization.__subclasses__(), category_name=filter_category)
        else:
            visualizations = Visualization.__subclasses__()

        return visualizations
    
    def get_visualizations_by_category(self, visualizations, category_name):
        """
        Get all visualizations within a category
        :param visualizations: list of Visualization subclasses to filter
        :param filter_category: str name of category to return visualizations for
        :return: A list of Visualization subclasses in the filter category
        """
        filtered_visualizations = []

        for vis in visualizations:
            if vis.category == category_name:
                filtered_visualizations.append(vis)

        return filtered_visualizations