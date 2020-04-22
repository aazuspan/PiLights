import random
import time

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class Fireflies(Visualization):
    name = 'Fireflies'
    description = 'Slowly fading green-yellow pixels over a dark background.'

    max_color = (150, 255, 0)
    fill_color = (5, 0, 10)
    fade_in_length = 750
    fade_out_length = 1500
    
    # Delay between fireflies in ms
    min_delay = 100
    max_delay = 500

    def render(self):
        self.pixels.fill(self.fill_color)
        self.pixels.show()

        firefly_index = random.randint(0, constants.PIXEL_COUNT - 1)

        # Set starting color
        faded_color = self.fill_color
        
        # Fade firefly color in
        for i in range(self.fade_in_length):
            faded_color = utils.interpolate_color(self.fill_color, self.max_color, i/self.fade_in_length)
            self.pixels[firefly_index] = utils.floatcolor2intcolor(faded_color)
            self.pixels.show()
        
        # Fade firefly color out
        for i in range(self.fade_out_length):
            faded_color = utils.interpolate_color(self.max_color, self.fill_color, i/self.fade_out_length)
            self.pixels[firefly_index] = utils.floatcolor2intcolor(faded_color)
            self.pixels.show()
            
        utils.sleep_ms(random.randint(self.min_delay, self.max_delay))
