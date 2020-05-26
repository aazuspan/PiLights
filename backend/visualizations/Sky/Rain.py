import random
import time

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class Rain(Visualization):
    name = 'Rain'
    description = 'Blue raindrops over a dark background'
    
    fill_color = (0, 2, 5)
    
    def __init__(self, pixels):
        super().__init__(pixels)
        
        self.raindrop_chance = 0.001
        self.raindrop_duration = 50
        
        self.array = [None for i in range(constants.PIXEL_COUNT)]
    
    #TODO: Set raindrop chance and duration with a very slow perlin noise to allow fluctuations in rain intensity
    def update(self):
        """
        """
        self.raindrop_chance = min(1, self.raindrop_chance + 0.001)
    
    def generate_raindrops(self):
        """
        Random chance of generating new raindrops in cells where there are no raindrops
        """
        for i, cell in enumerate(self.array):
            if not cell:
                if random.random() < self.raindrop_chance:
                    self.array[i] = Raindrop(self, i)
    
    def render(self):
        self.pixels.fill(self.fill_color)
        self.generate_raindrops()
        
        for cell in self.array:
            if cell:
                cell.fade()
                cell.render()
        
        self.pixels.show()

class Raindrop:
    color_range = {
        0: (150, 225, 255),
        1: (100, 150, 255),
        2: (50, 100, 150),
        3: (0, 50, 75),
        4: (0, 5, 10),
        5: (0, 2, 5),
    }
    
    def __init__(self, rain, index):
        self.rain = rain
        self.index = index
        self.rounds = 0
    
    @property
    def color(self):
        """
        Get the raindrop color by remapping and interpolating the number of rounds
        """
        remapped_rounds = utils.remap(self.rounds, 0, self.rain.raindrop_duration, 0, len(self.color_range))
        return utils.interpolate_color_from_dict(self.color_range, remapped_rounds)
    
    def fade(self):
        """
        Increment the number of rounds and remove the raindrop if over max rounds
        """
        self.rounds += 1
        
        if self.rounds >= self.rain.raindrop_duration:
            self.remove()
    
    def remove(self):
        """
        Remove the raindrop from the list of raindrops to prevent further rendering
        """
        self.rain.array[self.index] = None
    
    def render(self):
        self.rain.pixels[self.index] = self.color