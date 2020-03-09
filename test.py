import board
import neopixel
import time
import random

from rain import rain
from constants import *
from utils import *


red = [255, 0, 0]
blue = [0, 0, 255]
off = [0, 0, 0]
dark_blue = [0, 0, 50]

pixels = neopixel.NeoPixel(GPIO_PIN, PIXEL_COUNT, pixel_order=BRG, auto_write=False)


def light_trail(trail_length, head_color, trail_color, fill_color, delay_ms=0):
    """
    Draw a trail of light with a solid head and fading trail that leaves a fill behind
    """
    brightness_delta = -int(MAX_BRIGHTNESS / trail_length)
    
    for i in range(PIXEL_COUNT):
        pixels[i] = head_color
        
        for j in range(1, trail_length):
            fade_color = change_brightness(trail_color, brightness_delta * j)
            pixels[i - j] = fade_color

        pixels[i - j - 1] = fill_color
        
        time.sleep(delay_ms/1000)
        pixels.show()
    
    



def solid_fade(color, delay_ms=0, min_brightness=MIN_BRIGHTNESS, max_brightness=MAX_BRIGHTNESS):
    solid_fade_up(color, delay_ms, min_brightness, max_brightness)
    solid_fade_down(color, delay_ms, min_brightness, max_brightness)


def solid_fade_up(color, delay_ms, min_brightness, max_brightness):
    brightness_delta = 1
    
    # Change starting color to minimum version of color
    for band, val in enumerate(color):
        if val != 0:
            color[band] = min_brightness
            
    faded_color = color

    for i in range(min_brightness, max_brightness):
        faded_color = change_brightness(faded_color, brightness_delta)
        pixels.fill(faded_color)
        pixels.show()
        time.sleep(delay_ms/1000)


def solid_fade_down(color, delay_ms, min_brightness, max_brightness):
    brightness_delta = -1
    
    # Change starting color to maximum version of color
    for band, val in enumerate(color):
        if val != 0:
            color[band] = max_brightness
            
    faded_color = color

    for i in range(min_brightness, max_brightness):
        faded_color = change_brightness(faded_color, brightness_delta)
        pixels.fill(faded_color)
        pixels.show()
        time.sleep(delay_ms/1000)


def random_fades(r, g, b):
    random_colors = []
    
    for i in range(PIXEL_COUNT):
        random_colors.append({'color': None, 'delta': None})
        random_colors[i]['color'] = ([random.randint(0, r), random.randint(0, g), random.randint(0, b)])
        random_colors[i]['delta'] = random.choice([-1, 1])
        
    while True:
        for i in range(PIXEL_COUNT):
            pixel_color = random_colors[i]['color']
            current_delta = random_colors[i]['delta']
            
            pixels[i] = pixel_color
            
            if max(pixel_color) < 10:
                random_colors[i]['delta'] = 1
            elif max(pixel_color) > 250:
                random_colors[i]['delta'] = -1
            
            # TODO: Make this work on a per color basis, but also make a version of this that just fades all pixels randomly between a min and max solid color
            for band in range(len(random_color[i]['color'])):
                random_colors[i]['color'][band] = change_value(random_colors[i]['color'][band], random_colors[i]['delta'])
                
            #random_colors[i]['color'] = change_brightness(random_colors[i]['color'], random_colors[i]['delta'])
            
        #time.sleep(10/1000)
        pixels.show()

def twinkle():
    current_pixels = []
    # Indicates the probability of a pixel randomly being on or off
    on_off_choice = [0, 0, 0, 0, 0, 0, 0, 0, 1]
    
    for i in range(PIXEL_COUNT):
        current_pixels.append(random.choice(on_off_choice))
        
    while True:
        for i in range(PIXEL_COUNT):
            if current_pixels[i]:
                pixels[i] = (255, 255, 255)
            else:
                pixels[i] = (0, 0, 0)
            current_pixels[i] = random.choice(on_off_choice)
            
        
        time.sleep(500/1000)
        pixels.show()


while True:
    #twinkle()
    #random_fades(255, 255, 0)
    #rain(pixels)
    
    # Comet-y trail
    light_trail(trail_length=15, head_color=(255, 255, 255), trail_color=(255, 0, 255), fill_color=(0, 0, 15), delay_ms=45)
    # Firey trail
    light_trail(trail_length=15, head_color=(255, 100, 0), trail_color=(200, 100, 0), fill_color=(15, 5, 0), delay_ms=45)
    # Greenish trail
    light_trail(trail_length=15, head_color=(0, 255, 255), trail_color=(0, 255, 75), fill_color=(0, 20, 5), delay_ms=45)
    
    #solid_fade([255, 0, 255], 15, 25, 250)
    #solid_fade([0, 255, 255], 15, 25, 250)
    #solid_fade([255, 255, 0], 15, 25, 250)