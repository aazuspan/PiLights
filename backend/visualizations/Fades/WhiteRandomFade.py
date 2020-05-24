from backend.visualizations.Fades.GenericRandomFade import GenericRandomFade
from backend.visualizations.Visualization import Visualization
from backend import constants


class WhiteRandomFade(GenericRandomFade):
    name = "White Random Fade"
    description = "Randomly fading white pixels."
    hide = False
    color = [255, 255, 255]
    min_brightness = constants.MIN_BRIGHTNESS
    max_brightness = constants.MAX_BRIGHTNESS
