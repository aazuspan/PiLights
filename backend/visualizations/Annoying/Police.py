import time
import random

from backend import constants, utils
from backend.visualizations.Visualization import Visualization


class Police(Visualization):
    name = 'Stupid Police Lights'
    description = 'Flashing red and blue bands that rotate and randomly reverse direction.'
    
    color1 = (255, 0, 0)
    color2 = (0, 50, 255)
    color_width = 15
    reverse_chance = 0.01
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.index_offset = 0
        self.offset_direction = 1

    def render(self):
        count = 0
        
        for i in range(constants.PIXEL_COUNT):
            pixel_index = util.wraparound(i + self.index_offset)

            if count < self.color_width:
                self.pixels[pixel_index] = self.color1
            else:
                self.pixels[pixel_index] = self.color2
                
            count += 1
            
            if count >= self.color_width * 2:
                count = 0
            
        self.index_offset += self.offset_direction
        if random.random() < self.reverse_chance:
            self.offset_direction *= -1

        self.pixels.show()
