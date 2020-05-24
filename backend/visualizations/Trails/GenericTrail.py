from backend import constants
from backend.visualizations.Visualization import Visualization


class GenericTrail(Visualization):
    name = "Generic Trail"
    description = "Used to implement light trails."
    hide = True

    head_color = ()
    trail_color = ()
    fill_color = ()
    trail_length = 15
    delay_ms = 45
    brightness_delta = -int(constants.MAX_BRIGHTNESS / trail_length)
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.index = 0
    
    # Each render step, the trail should move forward and the head, trail, and fill should render
    def render(self):
        pass

"""
# THIS IS JUST HERE FOR REFERENCE. GET RID OF IT LATER
def light_trail(pixels, trail_length, head_color, trail_color, fill_color, delay_ms=0):
    brightness_delta = -int(constants.MAX_BRIGHTNESS / trail_length)

    for i in range(constants.PIXEL_COUNT):
        pixels[i] = head_color

        for j in range(1, trail_length):
            fade_color = change_brightness(trail_color, brightness_delta * j)
            pixels[i - j] = fade_color

        pixels[i - trail_length - 1] = fill_color

        time.sleep(delay_ms / 1000)
        pixels.show()
"""