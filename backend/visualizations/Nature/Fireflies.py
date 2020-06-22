import random

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class Fireflies(Visualization):
    name = 'Fireflies'
    description = 'Slowly fading green-yellow pixels over a dark background.'

    fill_color = (0, 0, 0)
    
    max_fireflies = 12
    firefly_chance = 0.01
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.fireflies = []
        self.pixels.fill(self.fill_color)
    
    def is_index_free(self, index):
        """
        Check if a given index has another firefly in or directly adjacent to it
        """
        for i in [-2, -1, 0, 1, 2]:
            if index + i in self.get_firefly_indexes():
                return False
        return True
    
    def get_firefly_indexes(self):
        """
        Return a list of all pixel indexes occupies by fireflies
        """
        indexes = []
        
        for firefly in self.fireflies:
            indexes.append(firefly.index)
            
        return indexes
        
        
    def render(self):
        """
        Randomly choose unoccupied indexes and create a new firefly, waiting the appropriate amount of time
        """
        if len(self.fireflies) < self.max_fireflies and random.random() < self.firefly_chance:
            self.generate_firefly()
        
        for firefly in self.fireflies:
            firefly.render()
        
        self.pixels.show()


    def generate_firefly(self):
        """
        Create a single firefly at a free location.
        """
        firefly_index = None
        
        while not firefly_index or not self.is_index_free(firefly_index):
            firefly_index = random.randint(0, constants.PIXEL_COUNT - 1)
        
        self.fireflies.append(Firefly(self, firefly_index))
            

class Firefly:
    max_color = (255, 255, 0)
    
    fade_in_duration = int(random.gauss(150, 25))
    fade_out_duration = (random.gauss(300, 50))
    
    def __init__(self, parent, index):
        self.parent = parent
        self.index = index
        self.rounds = 0
        self.min_color = self.parent.fill_color
        
    @property
    def color(self):
        """
        Interpolate firefly color, fading in or out based on the number of rounds.
        """
        if self.rounds < self.fade_in_duration:
            interp_color = utils.interpolate_color(self.min_color,
                                                   self.max_color,
                                                   self.rounds / self.fade_in_duration)
            
        else:
            interp_color = utils.interpolate_color(self.max_color,
                                                   self.min_color,
                                                   (self.rounds - self.fade_in_duration) / self.fade_out_duration)
        
        return interp_color
    
    def render(self):
        self.rounds += 1
        
        if self.rounds > self.fade_in_duration + self.fade_out_duration:
            self.remove()
        else:
            self.parent.pixels[self.index] = self.color
            
    def remove(self):
        """
        Remove the firefly from rendering
        """
        self.parent.fireflies.remove(self)