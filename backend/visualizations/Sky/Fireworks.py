import random

from backend.visualizations.Visualization import Visualization
from backend import constants
from backend import utils


class Fireworks(Visualization):
    name = 'Fireworks'
    description = 'Explosions of colored pixels.'
    
    fill_color = (0, 0, 0)
    firework_chance = 0.05
    
    colors = [
      (255, 100, 0),
      (255, 0, 150),
      (255, 25, 0),
      (255, 0, 25),
      (255, 0, 0),
    ]
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.fireworks = []

    def generate_fireworks(self):
        if random.random() < self.firework_chance:
            random_index = random.randint(0, constants.PIXEL_COUNT - 1)
            self.fireworks.append(Firework(random_index, random.choice(self.colors), self))
    
    def render(self):
        self.generate_fireworks()
        
        for firework in self.fireworks:
            firework.render()

        self.pixels.show()


class Firework:
    def __init__(self, center, color, vis, num_sparks=8):
        self.center = center
        self.color = color
        self.vis = vis
        self.num_sparks = num_sparks
        self.sparks = self.generate_sparks()
    
    def generate_sparks(self):
        return [VelocityPixel(self.center, self.color, self) for i in range(self.num_sparks)]
    
    def render(self):
        if self.sparks:
            for spark in self.sparks:
                spark.step()
        else:
            self.remove()
    
    def remove(self):
        self.vis.fireworks.remove(self)


class VelocityPixel:
    decceleration = 0.03
    
    mean_initial_velocity = 0.05
    sd_inital_velocity = 0.1 
    max_velocity = 0.25
    
    mean_duration = 100
    sd_duration = 50
    
    def __init__(self, i, color, parent):
        self.origin = i
        self.i = i
        self.starting_color = color
        self.color = color
        self.parent = parent
        self.velocity = random.gauss(self.mean_initial_velocity, self.sd_inital_velocity)
        self.direction = random.choice([-1, 1])
        self.rounds = 0
        self.duration = random.gauss(self.mean_duration, self.sd_duration)
        
    def deccelerate(self):
        self.velocity = utils.interpolate_value(self.velocity, 0, self.decceleration)
    
    def fade(self):
        self.color = utils.interpolate_color(self.starting_color, (0, 0, 0), self.rounds / self.duration)
        
    def move(self):
        self.i += self.velocity * self.direction
    
    def render(self):
        interp_pixels = utils.interpolate_pixels(self.i, self.color)
        
        for pixel in interp_pixels:
            if not utils.pixel_is_out_of_bounds(pixel[0]):
                self.parent.vis.pixels[pixel[0]] = pixel[1]
    
    def step(self):
        self.deccelerate()
        self.fade()
        
        self.move()
        self.rounds += 1
         
        if utils.pixel_is_out_of_bounds(self.i) or self.rounds > self.duration:
            self.remove()
        else:
            self.render()
    
    def remove(self):
        self.parent.sparks.remove(self)