import random

from backend.visualizations.Visualization import Visualization
from backend import constants
from backend import utils


class Particles(Visualization):
    name = 'Particles'
    description = 'Particles repel each other.'
    
    num_particles = 25
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.particles = [Particle(random.uniform(0, constants.PIXEL_COUNT), self) for i in range(self.num_particles)]

    def render(self):
        self.pixels.fill((0, 0, 0))
        
        for particle in self.particles:
            particle.step()
            particle.render()
        
        self.pixels.show()


class Particle:
    color = (255, 0, 0)
    influence_distance = 100
    
    max_speed = 10
    max_force = 0.5
    
    def __init__(self, position, parent):
        self.position = position
        self.parent = parent
        
        self.velocity = 0
        self.acceleration = 0
    
    def step(self):
        self.acceleration += self.separate()
        self.update()
    
    def separate(self):
        steer = 0
        count = 0
        
        for particle in self.parent.particles:
            distance = self.distance(particle)

            if 0 < abs(distance) < self.influence_distance:
                if distance < 0:
                    direction = -1
                elif distance > 0:
                    direction = 1
                else:
                    direction = 0
                    
                steer += direction / abs(distance)
                count += 1

        if count:
            steer /= count
        
        if steer:
            steer *= self.max_speed
            steer -= self.velocity
            steer = min(steer, self.max_force)

        return steer

    def update(self):
        self.velocity += self.acceleration
        self.velocity = min(self.velocity, self.max_speed)
        self.position += self.velocity
        self.edges()
        self.acceleration = 0
    
    def edges(self):
        if self.position < 0:
            self.position = 0
        elif self.position >= constants.PIXEL_COUNT - 1:
            self.position = constants.PIXEL_COUNT - 1
        
    def render(self):
        interp_pixels = utils.interpolate_pixels(self.position, self.color)
        
        for pixel in interp_pixels:
            if not utils.pixel_is_out_of_bounds(pixel[0]):
                self.parent.pixels[pixel[0]] = self.color
    
    def distance(self, other):
        return self.position - other.position
