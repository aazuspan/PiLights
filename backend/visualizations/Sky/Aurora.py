from backend import utils, constants
from backend.visualizations.Visualization import Visualization
from backend.visualizations.Noise import Noise


class Aurora(Visualization):
    name = 'Aurora'
    description = 'Aurora borealis lights.'
    
    def __init__(self, pixels):
        super().__init__(pixels)
        
        self.coarse_v_noise = Noise(0.001, 20, (-50, 80))
        self.v_noise = Noise(0.009, 2, (0, 150))
        self.rot_noise = Noise(0.03, 20, (-90, 0))
        self.interp_noise = Noise(-0.1, 10, (0.4, 1.0))
        self.g_noise = Noise(0.011, 2, (0, 255))
        self.b_noise = Noise(-0.012, 1, (0, 100))

    def render(self):
        for i in range(constants.PIXEL_COUNT):
            v = self.v_noise.value(i) + self.coarse_v_noise.value(i)
            g = self.g_noise.value(i)
            b = self.b_noise.value(i)

            # Apply fine value variations
            g = max(0, g-v)
            b = max(0, b-v)
        
            # Apply interpolation to make colors more similar
            b = int(utils.interpolate_value(b, g, self.interp_noise.value(i)))

            # Apply hue rotation
            color = (0, g, b)
            color = utils.rotate_rgb_hue(color, self.rot_noise.value(i))
            
            self.pixels[i] = color
            
        self.pixels.show()

        self.g_noise.update()
        self.b_noise.update()
        self.rot_noise.update()
        self.interp_noise.update()
        self.v_noise.update()
        self.coarse_v_noise.update()


