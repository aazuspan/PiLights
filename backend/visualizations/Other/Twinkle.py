import random
import time

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class Twinkle(Visualization):
    name = 'Twinkle'
    description = 'Random twinkling white pixels over a black background.'
    star_chance = 0.3
    shooting_star_chance = 0.0005
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.stars = self.generate_stars()
        self.shooting_stars = []

    def render(self):
        self.pixels.fill((0, 0, 0))
        
        self.generate_shooting_stars()
            
        for star in self.stars:
            star.twinkle()
            star.render()
            
        for shooting_star in self.shooting_stars:
            shooting_star.move_and_render()
            
        self.pixels.show()
    
    def generate_stars(self):
        """
        Generate a list of star pixel objects
        """
        stars = []
        for i in range(constants.PIXEL_COUNT):
            if random.random() < self.star_chance:
                stars.append(StarPixel(self, i))
        
        return stars

    def generate_shooting_stars(self):
        """
        Chance to generate a shooting star at a random location
        """
        if random.random() < self.shooting_star_chance:
            random_index = random.randint(0, constants.PIXEL_COUNT - 1)
            self.shooting_stars.append(ShootingStarPixel(self, random_index))

class StarPixel:
    max_min_brightness = 75
    max_brightness_delta = 25
    mean_delay = 0.6
    sd_delay = 0.2
    
    def __init__(self, parent, index):
        self.parent = parent
        self.index = index

        self.min_brightness = random.randint(1, self.max_min_brightness)
        # Bright stars should twinkle more
        if self.min_brightness > self.max_min_brightness//2:
            self.brightness_delta = random.randint(1, self.max_brightness_delta)
        else:
            self.brightness_delta = 0
        self.max_brightness = min(self.min_brightness + self.brightness_delta, 255)
        self.brightness = random.choice((self.min_brightness, self.max_brightness))
        
        self.delay_offset = random.random()
        self.twinkle_delay_s = random.normalvariate(self.mean_delay, self.sd_delay)
        self.last_twinkle_time = time.time() + self.delay_offset
    
    @property
    def color(self):
        return (self.brightness, self.brightness, self.brightness)
    
    def twinkle(self):
        """
        If it's time to change brightness, do so
        """
        current_time = time.time()
        
        if current_time - self.last_twinkle_time > self.twinkle_delay_s:
            if self.brightness == self.min_brightness:
                self.brightness = self.max_brightness
            else:
                self.brightness = self.min_brightness
            self.last_twinkle_time = current_time
            
    
    def render(self):
        self.parent.pixels[self.index] = self.color


class ShootingStarPixel:
    min_brightness = 0
    brightness_delta = 10
    
    def __init__(self, parent, index):
        self.parent = parent
        self.index = index
        
        self.max_brightness = random.randint(100, 255)
        self.brightness_direction = 1
        self.brightness = self.min_brightness
        self.direction = random.choice([-1, 1])
    
    def move_and_render(self):
        """
        The shooting star moves in the appropriate direction and changes brightness,
        then renders if still within bounds
        """
        self.index += self.direction
        
        if self.brightness_direction == 1:
            self.brightness = min(255, self.brightness + self.brightness_delta)
            if self.brightness >= self.max_brightness:
                self.brightness_direction = -1
        else:
            self.brightness = max(0, self.brightness - self.brightness_delta)

        if self.brightness <= 0 or util.pixel_is_out_of_bounds(self.index):
            self.remove()
        else:
            self.render()
        
    def render(self):
        self.parent.pixels[self.index] = (self.brightness, self.brightness, self.brightness)
        
    def remove(self):
        self.parent.shooting_stars.remove(self)
