import importlib
import pkgutil
import logging
import os
import threading
import time

from backend import constants
from backend.visualizations.Visualization import Visualization

logging.basicConfig(level=logging.DEBUG)


class Controller:
    # Time to wait for visualization threads to read kill_threads and die
    thread_kill_time = 1

    def __init__(self):
        self.categories = self.load_visualizations()
        self.current_vis = None
        self.thread_running = False
        self.kill_threads = False

    # TODO: Implement setting strip brightness
    def set_brightness(self, value):
        pass

    # TODO: Implement deiniting pixels
    def stop_render(self):
        self.stop_vis_threads()
        pass

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
    
    def get_categories(self):
        """
        Get a list of categories from loaded visualizations
        :return : A list of category names as strings
        """
        return list(self.categories.keys())

    def get_visualizations_by_category(self, category_name):
        """
        Get all visualizations within a category.
        :param category_name: str name of category to return visualizations for
        :return: A list of str names of Visualization subclasses in the filter category.
        """
        vis_list = []

        try:
            vis_list = self.categories[category_name]
        except KeyError:
            raise KeyError(f'Filter category name "{category_name}" is not a valid visualization category.')

        return vis_list

    def stop_vis_threads(self):
        """
        Kill any visualization threads that are currently running by setting the stop signal
        and waiting long enough for threads to see the signal and die. Wait time must be 
        long enough for all visualization loops to read the updated stop_vis_thread and die.
        """
        logging.debug('Killing threads...')
        self.kill_threads = True
        time.sleep(self.thread_kill_time)

        self.thread_running = False

    def start_vis(self, name):
        """
        Start a thread to run a visualization in the background. If a thread is already running,
        keep the thread running and just change the visualization to run. Otherwise, start a
        new thread.
        :param name: str name of visualization to run
        """
        self.current_vis = name

        if not self.thread_running:
            vis_thread = threading.Thread(target=self.run_vis, args=(name,))
            vis_thread.start()

    # TODO: Replace mock function with vis.render based on vis name
    def run_vis(self, name):
        """
        Run a visualization render method in the background until kill_threads is triggered
        :param name: str name of visualization to run
        """
        self.kill_threads = False

        while not self.kill_threads:
            logging.debug(f'Running {self.current_vis}')
            time.sleep(0.5)