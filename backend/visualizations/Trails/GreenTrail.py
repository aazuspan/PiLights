from backend.utils import light_trail
from backend.visualizations.Visualization import Visualization


class GreenTrail(Visualization):
    name = 'Green Trail'
    description = 'A light trail with a white head and green trail.'

    def render(self):
        light_trail(pixels=self.pixels,
                    trail_length=15,
                    head_color=(200, 255, 200),
                    trail_color=(0, 255, 100),
                    fill_color=(0, 15, 5),
                    delay_ms=45)
