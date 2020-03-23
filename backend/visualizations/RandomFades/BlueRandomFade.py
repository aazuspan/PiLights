from backend.visualizations.RandomFades.GenericRandomFade import GenericRandomFade
from backend.visualizations.Visualization import Visualization
from backend import constants


class BlueRandomFade(Visualization):
    name = "Blue Random Fade"
    description = "Randomly fading blue pixels."
    color = [0, 100, 255]
    min_brightness = constants.MIN_BRIGHTNESS
    max_brightness = constants.MAX_BRIGHTNESS
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.engine = GenericRandomFade(self.pixels, self.color, self.min_brightness, self.max_brightness) 
    
    def render(self):
        self.engine.render()