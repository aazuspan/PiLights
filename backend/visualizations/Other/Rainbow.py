import random

from backend.visualizations.Visualization import Visualization
from backend import constants
from backend import utils


class Rainbow(Visualization):
    name = 'Rainbow'
    description = 'Random shifting rainbow patterns.'

    def render(self):
        for i in range(constants.PIXEL_COUNT):
            r = random.randint(constants.MIN_BRIGHTNESS, constants.MAX_BRIGHTNESS)
            g = random.randint(constants.MIN_BRIGHTNESS, constants.MAX_BRIGHTNESS)
            b = random.randint(constants.MIN_BRIGHTNESS, constants.MAX_BRIGHTNESS)
            
            self.pixels[i] = ((r, g, b))
        
        self.pixels.show()
        utils.sleep_ms(800)
