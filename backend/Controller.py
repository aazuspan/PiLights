import importlib
import pkgutil

from backend import constants
from backend.visualizations.Visualization import Visualization


class Controller:
    def get_visualization_subclasses(self):
        """
        Import all visualization subclasses and return a list of them
        :return : A list of Visualization subclasses
        """
        for (module_loader, name, ispkg) in pkgutil.iter_modules([constants.VIS_DIR]):
            importlib.import_module('backend.visualizations.' + name, __package__)

        return Visualization.__subclasses__()
    
    def get_categories(self):
        """
        Get a list of categories from all available visualizations
        :return : A list of category names as strings
        """
        categories = []
        visualizations = self.get_visualization_subclasses()

        for vis in visualizations:
            if vis.category not in categories:
                categories.append(vis.category)
        
        return categories

    def get_visualizations_by_category(self, category_name):
        """
        Get all visualizations within a category, if provided. If not, return all.
        :param filter_category: str name of category to return visualizations for
        :return: A list of Visualization subclasses in the filter category, or all.
        """
        visualizations = self.get_visualization_subclasses()

        filtered_visualizations = []

        if not category_name:
            filtered_visualizations = visualizations
        else:
            for vis in visualizations:
                if vis.category == category_name:
                    filtered_visualizations.append(vis)

        return filtered_visualizations