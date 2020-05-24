from backend.visualizations.Fades.GenericRandomFade import GenericRandomFade
from backend.visualizations.Visualization import Visualization
from backend import constants


class OrangeRandomFade(GenericRandomFade):
    name = "Orange Random Fade"
    description = "Randomly fading orange pixels."
    hide = False
    color = [255, 80, 0]
    min_brightness = constants.MIN_BRIGHTNESS
    max_brightness = constants.MAX_BRIGHTNESS
