import random
import time

from backend import utils, constants
from backend.visualizations.Visualization import Visualization




class Fire(Visualization):
    name = 'Fire'
    description = 'Fire that grows outwards from the edges.'

    fire_temp = {
        1000: (255, 50, 1),
        2000: (255, 135, 0),
        3000: (255, 226, 0),
        4000: (255, 255, 0),
        5000: (255, 255, 198),
        6000: (235, 251, 255),
        7000: (177, 241, 255),
        8000: (118, 226, 255),
        9000: (63, 193, 255),
        10000: (19, 138, 255),
    }

    def render(self):
        pass
