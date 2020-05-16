from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class BinaryCounter(Visualization):
    name = 'Binary Counter'
    description = 'Count from 0 to 4.5 quadrillion in binary (this will take approximately 7 million years).'
    
    digit_spacing = 3
    color = (255, 255, 255)

    def __init__(self, pixels):
        super().__init__(pixels)
        self.count = 1
    
    def render(self):
        self.pixels.fill((10, 10, 10))
        binary_count = self.int2binary(self.count)

        for i, digit in enumerate(binary_count):
            if digit == "1":
                self.pixels[i * self.digit_spacing] = self.color
        
        self.pixels.show()
        utils.sleep_ms(500)
        self.count += 1

    def int2binary(self, x):
        """
        Convert an int to binary and return a string
        """
        return ("{0:b}".format(x))