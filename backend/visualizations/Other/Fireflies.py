import random
import time
import threading

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class Fireflies(Visualization):
    name = 'Fireflies'
    description = 'Slowly fading green-yellow pixels over a dark background.'

    max_color = (255, 255, 0)
    fill_color = (0, 0, 0)
    
    # Number of brightness steps during fade
    fade_in_length = 100
    fade_out_length = 50
    
    # Time delay between brightness steps during fade
    fade_delay = 25
    
    # Delay between fireflies in ms
    min_delay = 100
    max_delay = 1500
    
    max_fireflies = 15
    
    # List of currently active firefly indexes
    active_fireflies = []
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.pixels.fill(self.fill_color)
        self.pixels.show()
    
    @property
    def active_firefly_count(self):
        return len(self.active_fireflies)
    
    def is_index_free(self, index):
        """
        Check if a given index has another firefly in or directly adjacent to it
        """
        for i in [-1, 0, 1]:
            if index + i in self.active_fireflies:
                return False
        return True
        
        
    def render(self):
        """
        Randomly choose unoccupied indexes and create a new firefly, waiting the appropriate amount of time
        """
        firefly_index = None
        
        # Prevent having too many at one time, as this slows down the threads and causes issues
        if self.active_firefly_count < self.max_fireflies:
            # Prevent creating a firefly near another
            while not firefly_index or not self.is_index_free(firefly_index):
                firefly_index = random.randint(0, constants.PIXEL_COUNT - 1)
        
            self.create_firefly(firefly_index)
            utils.sleep_ms(random.randint(self.min_delay, self.max_delay))
        
        else:
            return

    def create_firefly(self, index):
        """
        Start a thread rendering a single firefly at a given index
        """
        firefly_thread = threading.Thread(target=self.render_firefly, args=(index,))
        firefly_thread.start()
        self.active_fireflies.append(index)

    def render_firefly(self, index):
        """
        Render a firefly by fading color in and back out
        """
        # Set starting color
        faded_color = self.fill_color
        
        # Fade firefly color in
        for i in range(self.fade_in_length):
            faded_color = utils.interpolate_color(self.fill_color, self.max_color, i/self.fade_in_length)
            self.pixels[index] = utils.floatcolor2intcolor(faded_color)
            self.pixels.show()
            utils.sleep_ms(self.fade_delay)
        
        # Fade firefly color out
        for i in range(self.fade_out_length):
            faded_color = utils.interpolate_color(self.max_color, self.fill_color, i/self.fade_out_length)
            self.pixels[index] = utils.floatcolor2intcolor(faded_color)
            self.pixels.show()
            utils.sleep_ms(self.fade_delay)
        
        # Ensure that pixel ends up fill color when done
        self.pixels[index] = self.fill_color
        
        self.active_fireflies.remove(index)
        return
