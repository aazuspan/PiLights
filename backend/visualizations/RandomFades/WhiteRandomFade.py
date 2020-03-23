from backend.visualizations.RandomFades.GenericRandomFade import GenericRandomFade
from backend.visualizations.Visualization import Visualization
from backend import constants


class WhiteRandomFade(Visualization):
    name = "White Random Fade"
    description = "Randomly fading white pixels."
    color = [255, 255, 255]
    min_brightness = constants.MIN_BRIGHTNESS
    max_brightness = constants.MAX_BRIGHTNESS
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.engine = GenericRandomFade(self.pixels, self.color, self.min_brightness, self.max_brightness) 
    
    def render(self):
        self.engine.render()
