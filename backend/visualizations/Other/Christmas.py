import random

from backend import constants, utils
from backend.visualizations.Visualization import Visualization


class Christmas(Visualization):
    name = 'Christmas Lights'
    description = 'Subtly fading green and red string lights.'

    spacing = 6

    def __init__(self, pixels):
        super().__init__(pixels)
        
        self.lights = []
        for i in range(0, constants.PIXEL_COUNT, self.spacing):
            if (i / self.spacing) % 2 == 0:
                primary_color = (255, 20, 0)
                secondary_color = (25, 0, 0)
                
            else:
                primary_color = (20, 255, 0)
                secondary_color = (0, 25, 0)
                
            self.lights.append(Light(self, i, primary_color, secondary_color))

    def render(self):
        for light in self.lights:
            light.fade()
            light.render()
        self.pixels.show()


class Light:
    def __init__(self, parent, index, primary_color, secondary_color):
        self.parent = parent
        self.index = index
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.color = self.primary_color
        self.fade_position = random.random()
        self.fade_direction = random.choice((-1, 1))
        self.fade_rate = random.gauss(0.005, 0.002)
        
    def fade(self):
        self.fade_position += self.fade_rate * self.fade_direction
        
        if self.fade_position >= 1:
            self.fade_direction = -1
        elif self.fade_position <= 0:
            self.fade_direction = 1
        
        self.color = utils.interpolate_color(self.primary_color, self.secondary_color, self.fade_position)
    
    def render(self):
        self.parent.pixels[self.index] = self.color