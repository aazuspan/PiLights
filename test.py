import neopixel
import random

from visualizations.Comet import Comet
import constants
from utils import *


red = [255, 0, 0]
blue = [0, 0, 255]
off = [0, 0, 0]
dark_blue = [0, 0, 50]

pixels = neopixel.NeoPixel(constants.GPIO_PIN, constants.PIXEL_COUNT, pixel_order=constants.BRG, auto_write=False)


def random_fades(r, g, b):
    random_colors = []
    
    for i in range(constants.PIXEL_COUNT):
        random_colors.append({'color': None, 'delta': None})
        random_colors[i]['color'] = ([random.randint(0, r), random.randint(0, g), random.randint(0, b)])
        random_colors[i]['delta'] = random.choice([-1, 1])
        
    while True:
        for i in range(constants.PIXEL_COUNT):
            pixel_color = random_colors[i]['color']
            current_delta = random_colors[i]['delta']
            
            pixels[i] = pixel_color
            
            if max(pixel_color) < 10:
                random_colors[i]['delta'] = 1
            elif max(pixel_color) > 250:
                random_colors[i]['delta'] = -1
            
            # TODO: Make this work on a per color basis, but also make a version of this that just fades all pixels randomly between a min and max solid color
            for band in range(len(random_colors[i]['color'])):
                random_colors[i]['color'][band] = change_value(random_colors[i]['color'][band], random_colors[i]['delta'])
                
            #random_colors[i]['color'] = change_brightness(random_colors[i]['color'], random_colors[i]['delta'])
            
        #time.sleep(10/1000)
        pixels.show()


def twinkle():
    current_pixels = []
    # Indicates the probability of a pixel randomly being on or off
    on_off_choice = [0, 0, 0, 0, 0, 0, 0, 0, 1]
    
    for i in range(constants.PIXEL_COUNT):
        current_pixels.append(random.choice(on_off_choice))
        
    while True:
        for i in range(constants.PIXEL_COUNT):
            if current_pixels[i]:
                pixels[i] = (255, 255, 255)
            else:
                pixels[i] = (0, 0, 0)
            current_pixels[i] = random.choice(on_off_choice)
            
        
        time.sleep(500/1000)
        pixels.show()


comet = Comet(pixels)

while True:
    comet.render()

    #twinkle()
    #random_fades(255, 255, 0)
    #rain(pixels)
    
    #solid_fade([255, 0, 255], 15, 25, 250)
    #solid_fade([0, 255, 255], 15, 25, 250)
    #solid_fade([255, 255, 0], 15, 25, 250)