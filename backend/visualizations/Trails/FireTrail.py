from backend.utils import light_trail
from backend.visualizations.Visualization import Visualization


class FireTrail(Visualization):
    name = 'Fire trail'
    description = 'A light trail with a red head and orange trail.'

    def render(self):
        light_trail(pixels=self.pixels,
                    trail_length=15,
                    head_color=(255, 100, 0),
                    trail_color=(200, 100, 0),
                    fill_color=(15, 5, 0),
                    delay_ms=45)
