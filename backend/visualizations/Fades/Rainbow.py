from backend.visualizations.Visualization import Visualization
from backend.visualizations.Noise import Noise
from backend import constants
from backend import utils


class Rainbow(Visualization):
    name = 'Rainbow'
    description = 'Random shifting rainbow pattern.'
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.rot_noise = Noise(0.01, 14, (-180, 180))

        
    def render(self):
        for i in range(constants.PIXEL_COUNT):
            color = (180, 255, 0)
            self.pixels[i] = utils.rotate_rgb_hue(color, self.rot_noise.value(i))
            
        self.pixels.show()
        self.rot_noise.update()

