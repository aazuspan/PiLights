import random
import time

from backend import utils, constants
from backend.visualizations.Visualization import Visualization




class Fire(Visualization):
    name = 'Fire'
    description = 'Fire that grows outwards from the edges.'

    fire_temp = {
        400: (5, 0, 0),
        500: (50, 0, 0),
        700: (75, 10, 0),
        800: (100, 25, 0),
        900: (150, 50, 5),
        1000: (200, 75, 10),
        1100: (225, 115, 20),
        1200: (255, 135, 50),
        1300: (255, 200, 75),
        1400: (255, 235, 100),
        1500: (255, 255, 150),
    }
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.fire_pixels = self.generate_pixels()
        self.temperatures = [0 for i in range(constants.PIXEL_COUNT)]

    def render(self):
        for pixel in self.fire_pixels:
            pixel.step()
        self.update_temperatures()
        self.pixels.show()
        utils.sleep_ms(0)

    def update_temperatures(self):
        """
        Update the list of temperatures for the fire from the fire pixels
        """
        for pixel in self.fire_pixels:
            self.temperatures[pixel.index] = pixel.temperature
        
    def generate_pixels(self):
        """
        Initialize and return a list of FirePixels
        """
        return [FirePixel(self, i) for i in range(constants.PIXEL_COUNT)]


class FirePixel:
    spark_chance = 0.001
    
    def __init__(self, fire, index):
        self.fire = fire
        self.index = index
        self.temperature = 0
    
    def is_out_of_bounds(self):
        """
        Check if the pixel is out of bounds of the fire
        :return : True if out of bounds, False if in bounds
        """
        if self.index < 0 or self.index > constants.PIXEL_COUNT - 1:
            return True
        return False
        
    def step(self):
        """
        Perform one frame of simulation for the fire pixel
        """
        self.chance_to_spark()
        self.update_temperature()
        self.move()
        
        self.render()
    
    def chance_to_spark(self):
        """
        Random chance to significantly increase temperature
        """
        if self.temperature < 1200:
            if random.random() < self.spark_chance:
                self.temperature = random.randint(1200, 1500)

    @property
    def color(self):
        """
        Use interpolation to select a color based on temperature from the table of temperature colors
        """
        interp_bounds = utils.get_interpolation_bounds(self.fire.fire_temp, self.temperature)
        interp_color = utils.interpolate_color(interp_bounds[0], interp_bounds[1], interp_bounds[2])
        
        return interp_color
    
    def move(self):
        """
        Random chance to shift position to left or right, staying within bounds of fire
        """
        position_offset = random.choice([0, 0, 0, 0, 0, 0, 0, 0, -1, 1])
        new_position = self.index + position_offset
        if new_position < 0 or new_position >= constants.PIXEL_COUNT:
            return
        self.index += position_offset
    
    def update_temperature(self):
        """
        Interpolate the temperature based on temperature of neighbouring pixels
        """
        neighbour_temp = self.get_average_neighbour_temperature()
        
        if self.temperature < neighbour_temp:
            self.temperature = utils.interpolate_value(self.temperature, neighbour_temp, 0.1)
        else:
            self.decrease_temperature()
        
    def decrease_temperature(self):
        """
        Reduce the temperature of the fire pixel
        """
        self.temperature = max(0, self.temperature - random.randint(1, 20))
    
    def get_average_neighbour_temperature(self):
        """
        Get the mean temperature of the two neighbouring fire pixels
        """
        neighbour_temps = []
        for neighbour_offset in [-1, 1]:
            try:
                neighbour_temps.append(self.fire.temperatures[self.index + neighbour_offset])
            except IndexError:
                pass
        return sum(neighbour_temps) / len(neighbour_temps)
    
    def render(self):
        self.fire.pixels[self.index] = self.color