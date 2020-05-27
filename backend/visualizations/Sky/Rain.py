import opensimplex
import random
import time

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class Rain(Visualization):
    name = 'Rain'
    description = 'Blue raindrops over a dark background'
    
    fill_color = (0, 5, 15)
    
    min_raindrop_chance = 0.0005
    max_raindrop_chance = 0.05
    
    min_raindrop_duration = 15
    max_raindrop_duration = 100
    
    def __init__(self, pixels):
        super().__init__(pixels)
        
        self.noise_index = 0
        self.noise_interval = 0.001
        self.perlin_noise = opensimplex.OpenSimplex()
        
        self.intensity = 0.0

        self.array = [random.choice([None, Raindrop(self, i)]) for i in range(constants.PIXEL_COUNT)]
    
    def update(self):
        """
        Update rain intensity using Perlin noise
        """
        noise = self.perlin_noise.noise2d(self.noise_index, 0)
        self.intensity = utils.remap(noise, -1, 1, 0, 1)
        self.noise_index += self.noise_interval
    
    @property
    def raindrop_chance(self):
        """
        Interpolate raindrop chance based on rain intensity. More intense == more raindrops
        """
        return utils.interpolate_value(self.min_raindrop_chance, self.max_raindrop_chance, self.intensity)
    
    @property
    def raindrop_duration(self):
        """
        Interpolate raindrop chance based on rain intensity. More intense == faster raindrops
        """
        return utils.interpolate_value(self.max_raindrop_duration, self.min_raindrop_duration, self.intensity)
    
    def generate_raindrops(self):
        """
        Random chance of generating new raindrops in cells where there are no raindrops
        """
        raindrop_chance = self.raindrop_chance
        
        for i, cell in enumerate(self.array):
            if random.random() < raindrop_chance:
                self.array[i] = Raindrop(self, i)
    
    def render(self):
        self.update()
        self.pixels.fill(self.fill_color)
        self.generate_raindrops()
        
        for cell in self.array:
            if cell:
                cell.fade()
                cell.render()
        
        self.pixels.show()


class Raindrop:
    color_range = {
        0: (200, 255, 255),
        1: (100, 150, 255),
        2: (50, 100, 150),
        3: (0, 50, 75),
        4: (0, 20, 50),
        5: (0, 5, 15),
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