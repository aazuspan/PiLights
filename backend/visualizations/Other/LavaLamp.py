from backend.visualizations.Visualization import Visualization
from backend import constants
from backend import utils

import opensimplex


class LavaLamp(Visualization):
    name = 'Lava Lamp'
    description = 'Red and purple blobs.'
    
    scale = 16
    threshold = 0
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.y = 0
        self.color_offset = 0.1
        self.noise = opensimplex.OpenSimplex()

    def render(self):
        for i in range(constants.PIXEL_COUNT):
            noise = self.noise.noise2d(i / self.scale, self.y / self.scale)
            val = 0 if noise < self.threshold else noise
            color = int(utils.remap(val, 0, 1, 0, 255))
            
            if not color:
                color = (5, 2, 0)
                color = (0, 0, 0)
            else:
                color = (color, color//4, 0)
                
            color_noise = self.noise.noise2d((i + self.color_offset) / self.scale, 0)
            color = utils.rotate_rgb_hue(color, utils.remap(color_noise, -1, 1, -60, 0))
            
            self.pixels[i] = color
            
        self.pixels.show()
        
        self.color_offset += 0.05
        self.y += 0.05

