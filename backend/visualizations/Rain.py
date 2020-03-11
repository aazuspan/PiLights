import random
import time

from backend import utils, constants
from backend.visualizations.Visualization import Visualization
from backend.visualizations import categories


class Rain(Visualization):
    name = 'Rain'
    description = 'Random fading blue pixels over a light blue background.'
    category = categories.OTHER

    drop_color = (100, 150, 200)
    fill_color = (0, 15, 15)
    min_drops = 1
    max_drops = 3
    min_delay = 0
    max_delay = 15
    fade_length = 90

    def render(self):
        self.pixels.fill(self.fill_color)
        self.pixels.show()

        num_drops = random.randint(self.min_drops, self.max_drops)
        drop_indexes = [random.randint(0, constants.PIXEL_COUNT - 1) for i in range(num_drops)]

        faded_color = self.drop_color
        brightness_delta = -int(constants.MAX_BRIGHTNESS / self.fade_length)

        # Fade drop color
        for i in range(0, self.fade_length):
            faded_color = utils.change_brightness(faded_color, brightness_delta, 15)

            # Set all drops simultaneously
            for drop_index in drop_indexes:
                self.pixels[drop_index] = faded_color

            self.pixels.show()

        time.sleep(random.randint(self.min_delay, self.max_delay)/1000)
