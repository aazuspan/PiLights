import importlib
import pkgutil
import pywemo
import logging
import os
import threading
import time

from backend.visualizations.Visualization import Visualization
from backend.memory.Memory import Memory
from backend import constants

if not constants.DEV_MODE:
    import neopixel

logging.basicConfig(level=logging.DEBUG)


class Controller:
    # Time to wait for visualization threads to read kill_threads and die
    thread_kill_time = 2.5

    def __init__(self):
        if not constants.DEV_MODE:
            self.pixels = neopixel.NeoPixel(constants.GPIO_PIN,
                                            constants.PIXEL_COUNT,
                                            pixel_order=constants.BRG,
                                            auto_write=False)
            self.visualization_categories = self.load_visualizations()

        else:
            self.pixels = None
            self.visualization_categories = {}

        self.visualization_categories = self.load_visualizations()
        self.current_vis = None
        self.thread_running = False
        self.kill_threads = False
        self.memory = Memory()
        self.wemos = self.scan_for_wemos()
        self.wemos = []
        self.on = False
    
    def get_current_vis(self):
        """
        If a visualization is playing, return a dictionary with its name and category
        """
        if self.current_vis:
            return {'name': self.current_vis.name, 'category': self.current_vis.category}
        return None

    def set_brightness(self, value):
        logging.info(f"Setting brightness to {value}")
        self.pixels.brightness = int(value)/255

    def stop_render(self):
        logging.info("Stopping rendering.")
        self.stop_vis_threads()
            
    def clear_pixels(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
    
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

                    if issubclass(vis_class, Visualization):
                        if not vis_class.hide:
                            if folder.name not in categories:
                                categories[folder.name] = [vis_class]
                            else:
                                categories[folder.name].append(vis_class)

                except AttributeError:
                    vis_class = None
                    logging.warn(f'{name} does not contain class {name}. If the file is not a visualization,'
                        ' ignore this warning. Otherwise, the visualization class name must be the same as'
                        ' the file name.')
        return categories
    
    @property
    def categories(self):
        """
        Get a list of categories from loaded visualizations
        :return : A list of category names as strings
        """
        return list(self.visualization_categories.keys())

    @property
    def visualizations(self):
        """
        Get a list of all loaded Visualization subclasses
        :return : A list of Visualization subclasses
        """
        visualizations = []

        for category in self.visualization_categories:
            for vis in self.visualization_categories[category]:
                visualizations.append(vis)
        return visualizations

    def get_visualizations_by_category(self, category_name):
        """
        Get all visualizations within a category.
        :param category_name: str name of category to return visualizations for
        :return: A list of str names of Visualization subclasses in the filter category.
        """
        vis_list = []

        try:
            vis_list = self.visualization_categories[category_name]
        except KeyError:
            raise KeyError(f'Filter category name "{category_name}" is not a valid visualization category.')

        return vis_list

    def stop_vis_threads(self):
        """
        Kill any visualization threads that are currently running by setting the stop signal
        and waiting long enough for threads to see the signal and die. Wait time must be 
        long enough for all visualization loops to read the updated stop_vis_thread and die.
        """
        self.kill_threads = True
        self.current_vis = None
        time.sleep(self.thread_kill_time)

        self.thread_running = False

    def turn_off(self):
        """
        Turn off the switched wemo.
        """
        self.set_switched_wemo_state(False)        

    def turn_on(self):
        """
        Turn on the switched WEMO, if one is set
        """
        self.set_switched_wemo_state(True)

    def start_vis(self, name):
        """
        Start a thread to run a visualization in the background. If a thread is already running,
        keep the thread running and just change the visualization to run. Otherwise, start a
        new thread.
        :param name: str name of visualization to run
        """

        vis_class = self.get_vis_by_name(name)
        
        if self.thread_running:
            self.stop_render()
            
        logging.info(f"Starting {name}")
        self.current_vis = vis_class(pixels=self.pixels)
        vis_thread = threading.Thread(target=self.run_vis)
        vis_thread.start()
        
        self.set_switched_wemo_state(True)

    def scan_for_wemos(self):
        """
        Scan the network for WEMO devices and return them
        :return : A list of WEMO devices
        """
        wemos = []
        
        logging.info('Discovering WEMO devices on network...')
        try:
            wemos = pywemo.discover_devices()
            logging.info('{} WEMO devices successfully discovered.'.format(len(wemos)))

        except Exception as e:
            logging.exception(("An error occurred while scanning for WEMO devices. If any"
            " WEMO names were changed, try unplugging and replugging the WEMO, and then"
            " restarting this program."))

        return wemos

    def get_wemo_by_mac(self, mac):
        """
        Get the Wemo device based on its mac address
        :param mac: string Mac address of the Wemo device on the network
        :param state: pywemo.Switch wemo device
        """
        for wemo in self.wemos:
            if wemo.mac == mac:
                return wemo
        return None

    def set_wemo_state(self, mac, state):
        """
        Set the power state of a Wemo device based on its mac address
        :param mac: string Mac address of the Wemo device on the network
        :param state: bool New power state of the Wemo
        """
        device = self.get_wemo_by_mac(mac)
        
        if device:
            device.set_state(state)

    def get_switched_wemo(self):
        """
        If a switched WEMO is set in settings, return a dictionary of the WEMOs label and mac address. If not, return None
        """
        switch_wemo = self.memory.load_setting('switch_wemo')
        return switch_wemo['current_value']

    def set_switched_wemo_state(self, state):
        """
        Set the power state of the switched WEMO, if one is set in settings
        :param state: bool power state to set WEMO device to
        """
        switched_wemo = self.get_switched_wemo()
        if switched_wemo:
            self.set_wemo_state(switched_wemo['mac'], state)

    def get_switched_wemo_state(self):
        """
        If a switched WEMO is set in settings, return its current power state. If not, return 1
        """
        switched_wemo = self.get_switched_wemo()
        if switched_wemo['mac']:
            device = self.get_wemo_by_mac(switched_wemo['mac'])
            if device:
                return device.get_state()
        return 1

    def run_vis(self):
        """
        Run a visualization render method in the background until kill_threads is triggered
        """
        self.kill_threads = False
        self.thread_running = True

        if constants.DEV_MODE:
            return
            
        while not self.kill_threads:
            self.current_vis.render()
            
        self.clear_pixels()

    def get_vis_by_name(self, name):
        """
        Get and return a Visualization subclass whose name attribute matches the given name
        :param name: str name of visualization to return
        :return : class of Visualization subclass
        """
        for vis in self.visualizations:
            try:
                if vis.name == name:
                    return vis
            except AttributeError:
                logging.error(f'{vis} does not contain a name attribute! Ensure that all Visualization subclasses have a name.')
        
        return None
