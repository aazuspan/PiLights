import random

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class Fire(Visualization):
    name = 'Fire'
    description = 'Fire that flickers and flares up.'

    fire_temp = {
        0: (15, 0, 0),
        200: (20, 5, 0),
        400: (25, 10, 0),
        500: (50, 15, 0),
        700: (75, 20, 0),
        800: (100, 25, 5),
        900: (150, 50, 10),
        1000: (200, 75, 15),
        1100: (225, 115, 20),
        1200: (255, 135, 25),
        1300: (255, 150, 50),
        1400: (255, 175, 60),
        1500: (255, 200, 75),
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
        utils.sleep_ms(50)

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
    spark_chance = 0.00005
    flare_chance = 0.15
    temp_interp_weight = 0.21
    temp_decrease = 41
    min_flare_temp = 50
    max_flare_temp = 175
    min_temperature = 400
    max_temperature = 1500
    
    def __init__(self, fire, index):
        self.fire = fire
        self.index = index
        self.temperature = random.randint(0, self.max_temperature/2)
        
    def step(self):
        """
        Perform one frame of simulation for the fire pixel
        """

        self.update_temperature()
        self.render()
    
    def chance_to_spark(self):
        """
        Random chance to significantly increase temperature
        """
        if random.random() < self.spark_chance:
            self.spark()
            
    def spark(self):
        """
        Increase temperature to max
        """
        self.temperature = self.max_temperature
        
    def chance_to_flare(self):
        """
        Random chance to increase temperature
        """
        if random.random() < self.flare_chance:
            self.flare()
            
    def flare(self):
        """
        Increase temperature by a random amount
        """
        self.temperature = min(self.max_temperature, self.temperature + random.randint(self.min_flare_temp, self.max_flare_temp))
        
    @property
    def color(self):
        """
        Use interpolation to select a color based on temperature from the table of temperature colors
        """
        interp_bounds = utils.get_interpolation_bounds(self.fire.fire_temp, self.temperature)
        interp_color = utils.interpolate_color(interp_bounds[0], interp_bounds[1], interp_bounds[2])
        
        return interp_color
    
    def update_temperature(self):
        """
        Chance to flare up, interpolate the temperature of neighbouring pixels, and decrease temperature
        """
        self.chance_to_flare()
        self.chance_to_spark()
        
        neighbour_temp = self.get_average_neighbour_temperature()
        
        if self.temperature < neighbour_temp:
            self.temperature = utils.interpolate_value(self.temperature, neighbour_temp, self.temp_interp_weight)
        else:
            self.decrease_temperature()
        
    def decrease_temperature(self):
        """
        Reduce the temperature of the fire pixel
        """
        self.temperature = max(self.min_temperature, self.temperature - self.temp_decrease)
    
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