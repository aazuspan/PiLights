from backend.visualizations.Visualization import Visualization
from backend import constants
from backend import utils


class SwirlingFade(Visualization):
    name = 'Swirling Fade'
    description = 'A swirling color fade between blue, purple, and green.'
    
    fill_color = (0, 0, 0)
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.trails = [
            BlurryTrail(0, (255, 0, 0), (0, 25, 255), 77, self),
            BlurryTrail(75, (0, 255, 0), (0, 25, 255), 77, self),
        ]

    def render(self):
        self.pixels.fill(self.fill_color)
        
        for trail in self.trails:
            trail.move()
            trail.render()
        
        self.pixels.show()
        utils.sleep_ms(50)
        

class BlurryTrail:
    def __init__(self, i, center_color, edge_color, kernel_width, parent):
        self.i = i
        self.center_color = center_color
        self.edge_color = edge_color
        self.kernel_width = kernel_width
        self.parent = parent
    
    def move(self):
        if self.i >= constants.PIXEL_COUNT:
            self.i = 0
            
        self.i += 1
        
    def render(self):
        blurred_pixels = utils.get_blurred_pixels(self.i, self.center_color, self.edge_color, self.kernel_width)
        
        for pixel in blurred_pixels:
            index = utils.wraparound(pixel[0])
            self.parent.pixels[index] = pixel[1]