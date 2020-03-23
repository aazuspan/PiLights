from backend.visualizations.RandomFades.GenericRandomFade import GenericRandomFade
from backend.visualizations.Visualization import Visualization
from backend import constants


class OrangeRandomFade(Visualization):
    name = "Orange Random Fade"
    description = "Randomly fading orange pixels."
    color = [255, 80, 0]
    min_brightness = constants.MIN_BRIGHTNESS
    max_brightness = constants.MAX_BRIGHTNESS
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.engine = GenericRandomFade(self.pixels, self.color, self.min_brightness, self.max_brightness) 
    
    def render(self):
        self.engine.render()
