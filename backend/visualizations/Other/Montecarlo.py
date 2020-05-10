import random

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class Montecarlo(Visualization):
    name = 'Montecarlo'
    description = 'Randomly bouncing ball.'
    
    corners = [35, 78, 83, 93, 119, 128, 133]
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.ball = Ball(self, 0)

    def render(self):
        self.pixels.fill((0, 15, 25))
        self.ball.move()
        self.ball.render()
        self.pixels.show()
        

class Ball:
    color = (255, 255, 255)
    
    def __init__(self, parent, index):
        self.parent = parent
        self.index = index
        self.direction = 1
        self.returning_home = False
    
    def choose_random_direction(self):
        if self.index in self.parent.corners:
            direction = random.choice([-1, 1, 1, 1])
        else:
            direction = self.direction
            
        if direction == -1:
            self.returning_home == True
            
        return direction
    
    def move(self):
        if self.index == 0:
            self.direction = 1
        elif self.index == 150:
            self.direction = -1
            
        if self.direction == 1:
            self.direction = self.choose_random_direction()
                
        self.index += self.direction

    
    def render(self):
        self.parent.pixels[self.index] = self.color