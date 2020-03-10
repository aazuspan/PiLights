from backend.utils import light_trail
from backend.visualizations.Visualization import Visualization


class Comet(Visualization):
    name = 'Comet'
    description = 'A light trail with a white head and blue trail.'

    def render(self):
        light_trail(pixels=self.pixels,
                    trail_length=15,
                    head_color=(255, 255, 255),
                    trail_color=(255, 0, 255),
                    fill_color=(0, 0, 15),
                    delay_ms=45)
