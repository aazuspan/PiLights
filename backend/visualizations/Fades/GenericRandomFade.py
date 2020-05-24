import random
import time

from backend.utils import sleep_ms
from backend import utils
from backend import constants
from backend.visualizations.Visualization import Visualization


class GenericRandomFade(Visualization):
    name = "Generic Random Fade"
    description = "Used to implement colored random fades."
    hide = True
    color = None
    min_brightness = None
    max_brightness = None
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.pixel_list = self.build_pixels()
            
    def build_pixels(self):
        """
        Build a randomized list of pixel brightnesses and directions
        """
        pixel_list = []
        for i in range(constants.PIXEL_COUNT):
            brightness = random.randint(self.min_brightness, self.max_brightness)
            direction = random.choice((-1, 1))
            color = self.color
            pixel_list.append(FadingPixel(i, self.color, brightness, direction, self.min_brightness, self.max_brightness))
            
        return pixel_list
        
    def render(self):
        for pixel in self.pixel_list:
            pixel.fade()
            self.pixels[pixel.index] = pixel.get_color()
        self.pixels.show()
        sleep_ms(0)


class FadingPixel:
    def __init__(self, index, color, brightness, direction, min_brightness, max_brightness):
        self.index = index
        self.starting_color = color
        self.brightness = brightness
        self.direction = direction
        self.min_brightness = min_brightness
        self.max_brightness = max_brightness
    
    def get_color(self):
        """
        Adjust the color of each band of the pixel based on the brightness of the pixel
        :return : A list of ints in form [r, g, b]
        """
        adjusted_color = []
        for band in self.starting_color:
            adjusted_band = int(utils.remap(band,
                                            self.min_brightness,
                                            self.max_brightness,
                                            self.min_brightness,
                                            self.brightness))
            adjusted_color.append(adjusted_band)
        return adjusted_color
        
    def change_direction(self):
        """
        Reverse the direction of brightness change
        """
        self.direction *= -1
        
    def fade(self):
        if self.brightness + self.direction > self.max_brightness:
            self.brightness = self.max_brightness
            self.change_direction()
        elif self.brightness + self.direction < self.min_brightness:
            self.brightness = self.min_brightness
            self.change_direction()
        else:
            self.brightness += self.direction
