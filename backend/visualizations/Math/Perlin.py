import opensimplex
import random

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class Perlin(Visualization):
    name = 'Perlin'
    description = 'Perlin noise.'
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.perlin_noise = opensimplex.OpenSimplex()
        self.offset = 0

    def render(self):
        for i in range(constants.PIXEL_COUNT):
            noise = self.perlin_noise.noise2d(i + self.offset, 0)
            color = utils.floatcolor2intcolor((255 * noise, 255 * noise, 255 * noise))
            
            self.pixels[i] = color
            
        self.pixels.show()
        
        noise_offset = 0.006
        self.offset += noise_offset

