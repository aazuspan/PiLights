import random
import time

from backend import constants, utils
from backend.visualizations.Visualization import Visualization


class ChristmasFlash(Visualization):
    name = 'Flashing Christmas Lights'
    description = 'Flashing green and red string lights.'

    spacing = 6

    def __init__(self, pixels):
        super().__init__(pixels)
        
        self.lights = []
        for i in range(0, constants.PIXEL_COUNT, self.spacing):
            if (i / self.spacing) % 2 == 0:
                primary_color = (255, 20, 0)
                secondary_color = (20, 255, 0)
                
            else:
                primary_color = (20, 255, 0)
                secondary_color = (255, 20, 0)
                
            self.lights.append(Light(self, i, primary_color, secondary_color))

    def render(self):
        for light in self.lights:
            light.update_state()
            light.render()
        self.pixels.show()


class Light:
    def __init__(self, parent, index, primary_color, secondary_color):
        self.parent = parent
        self.index = index
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.colors = [primary_color, secondary_color]
        self.state = random.choice([0, 1])
        self.state_change_time = random.gauss(1, 0.1)
        self.last_change_time = time.time()
        
    def update_state(self):
        current_time = time.time()
        
        if current_time - self.last_change_time > self.state_change_time:
            self.state = not self.state
            self.last_change_time = current_time
    
    @property
    def color(self):
        return self.colors[self.state]
        
    def render(self):
        self.parent.pixels[self.index] = self.color