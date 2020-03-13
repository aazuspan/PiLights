import importlib
import pkgutil
import os

from backend import constants
from backend.visualizations.Visualization import Visualization


class Controller:
    def __init__(self):
        self.categories = self.load_visualizations()

    def load_visualizations(self):
        """
        Import all Visualization subclasses in subfolders of the visualization directory and return a dictionary 
        of Visualization subclass lists for each category folder.

        Note that category names come from folder names.

        :return : A dictionary of {category_name: [Visualization subclasses]}
        """
        subfolders= [f for f in os.scandir(constants.VIS_DIR) if f.is_dir()]

        categories = {}

        for folder in subfolders:
            for (module_loader, name, ispkg) in pkgutil.iter_modules([folder.path]):
                module = importlib.import_module(f'backend.visualizations.{folder.name}.{name}', __package__)

                try:
                    vis_class = getattr(module, name)

                    # If it is a subclass of Visualization
                    if Visualization in vis_class.__bases__:
                        if folder.name not in categories:
                            categories[folder.name] = [vis_class]
                        else:
                            categories[folder.name].append(vis_class)

                # Catch errors if a file doesn't contain a class of the same name
                except AttributeError:
                    vis_class = None

        return categories

    def get_visualizations(self):
        """
        Return all loaded Visualization subclasses
        :return : A list of Visualization subclasses
        """
        vis_list = []

        for vis_category in self.categories.values():
            for vis in vis_category:
                vis_list.append(vis)

        return vis_list
    
    def get_categories(self):
        """
        Get a list of categories from loaded visualizations
        :return : A list of category names as strings
        """
        return list(self.categories.keys())

    def get_visualizations_by_category(self, category_name):
        """
        Get all visualizations within a category, if provided. If not, return all.
        :param filter_category: str name of category to return visualizations for
        :return: A list of Visualization subclasses in the filter category, or all.
        """
        vis_list = []

        if not category_name:
            vis_list = self.get_visualizations()
        elif category_name in list(self.categories.keys()):
            vis_list = self.categories[category_name]

        return vis_list