import random
import time

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class Twinkle(Visualization):
    name = 'Twinkle'
    description = 'Random fading white pixels over a black background.'


    def render(self):
        pass
