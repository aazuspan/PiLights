from backend import constants, utils
from backend.visualizations.Visualization import Visualization


class GenericTrail(Visualization):
    name = "Generic Trail"
    description = "Used to implement light trails."
    hide = True

    head_color = (255, 255, 255)
    tail_color = (255, 0, 0)
    fill_color = (0, 0, 255)
    trail_length = 60
    delay_ms = 40
    
    brightness_delta = -int(constants.MAX_BRIGHTNESS / trail_length)
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.trail_pixels = self.generate_trail()
        
    def generate_trail(self):
        """
        Generate the pixels that make up the trail, including the head. Trail colors are
        interpolated between the defined tail color and fill color.
        """
        new_pixels = []
        
        new_pixels.append(Pixel(self, self.trail_length, self.head_color))
        
        for i in range(0, self.trail_length):
            interp_color = utils.interpolate_color(self.fill_color, self.tail_color, i/self.trail_length)
            new_pixels.append(Pixel(self, i, interp_color))
        
        return new_pixels
    
    def render(self):
        self.pixels.fill(self.fill_color)
        
        for pixel in self.trail_pixels:
            pixel.move()
            pixel.render()
        
        self.pixels.show()
        utils.sleep_ms(self.delay_ms)
        

class Pixel:
    def __init__(self, parent, index, color):
        self.parent = parent
        self.index = index
        self.color = color
        
    def move(self):
        self.index = utils.wraparound(self.index + 1)
        
    def render(self):
        self.parent.pixels[self.index] = self.color
