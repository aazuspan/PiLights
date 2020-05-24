from backend.visualizations.Fades.GenericRandomFade import GenericRandomFade
from backend.visualizations.Visualization import Visualization
from backend import constants


class BlueRandomFade(GenericRandomFade):
    name = "Blue Random Fade"
    description = "Randomly fading blue pixels."
    hide = False
    color = [0, 100, 255]
    min_brightness = constants.MIN_BRIGHTNESS
    max_brightness = constants.MAX_BRIGHTNESS
