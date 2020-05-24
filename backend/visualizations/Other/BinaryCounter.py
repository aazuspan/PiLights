from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class BinaryCounter(Visualization):
    name = 'Binary Counter'
    description = 'Count from 0 to 4.5 quadrillion in binary (this will take approximately 7 million years).'
    
    digit_spacing = 3
    fill_color = (0, 8, 2)
    off_color = (0, 35, 10)
    on_color = (5, 255, 50)
    ms_delay = 500

    def __init__(self, pixels):
        super().__init__(pixels)
        self.count = 1
    
    def render(self):
        self.pixels.fill(self.fill_color)
        binary_count = utils.int2binary(self.count)

        for i, digit in enumerate(binary_count):
            if digit == "1":
                self.pixels[i * self.digit_spacing] = self.on_color
            else:
                self.pixels[i * self.digit_spacing] = self.off_color
        
        self.pixels.show()
        utils.sleep_ms(self.ms_delay)
        self.count += 1
