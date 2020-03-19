import random
import time

from backend.utils import sleep_ms
from backend import utils
from backend import constants
from backend.visualizations.Visualization import Visualization


class OrangeFade(Visualization):
    name = 'Orange Fade'
    description = 'Randomly fading orange lights.'
    color = [255, 100, 0]
    
    def __init__(self,
                 pixels,
                 min_brightness=constants.MIN_BRIGHTNESS,
                 max_brightness=constants.MAX_BRIGHTNESS):
        super().__init__(pixels)
        self.min_brightness = min_brightness
        self.max_brightness = max_brightness
        self.pixel_list = self.build_pixels()
            
    def build_pixels(self):
        pixel_list = []
        for i in range(constants.PIXEL_COUNT):
            brightness = random.randint(self.min_brightness, self.max_brightness)
            direction = random.choice((-1, 1))
            color = [random.randint(140, 150), random.randint(150, 255), random.randint(150, 255)]
            pixel_list.append(FadingPixel(i, color, brightness, direction, 0, 255))
            
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
