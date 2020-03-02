import random
import time

from constants import *
from utils import *


def rain(pixels):
    drop_color = (100, 150, 200)
    fill_color = (0, 15, 15)
    min_drops = 1
    max_drops = 3
    min_delay = 0
    max_delay = 50
    fade_length = 70
    pixels.fill(fill_color)
    pixels.show()
    
    
    # Number of simultaneous drops
    num_drops = random.randint(min_drops, max_drops)
    # Pre-select the drops
    drop_indexes = [random.randint(0, PIXEL_COUNT -1) for i in range(num_drops)]
    
    faded_color = drop_color
    brightness_delta = -int(MAX_BRIGHTNESS/fade_length)
    
    #fade_length = random.randint(20, 200)
    # Fade drop color
    for i in range(0, fade_length):
        faded_color = change_brightness(faded_color, brightness_delta, 15)
        
        # Set all drops simultaneously
        for drop_index in drop_indexes:
            pixels[drop_index] = faded_color
        
        pixels.show()

    time.sleep(random.randint(min_delay, max_delay)/1000)