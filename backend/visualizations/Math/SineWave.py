import math

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class SineWave(Visualization):
    name = 'Sine Wave'
    description = 'Pixel brightness determined by a moving sine wave.'
    offset_interval = 0.01
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.offset = 0

    def render(self):
        for i in range(constants.PIXEL_COUNT):
            sin = int(utils.remap(math.sin(i/4 + self.offset), -1, 1, 0, 255))
            self.pixels[i] = (0, sin//2, sin)

        self.offset += self.offset_interval
        self.pixels.show()


