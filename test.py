import board
import neopixel
import time
import random

from rain import rain
from constants import *


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
        time.sleep(delay_ms/1000)


while True:
    rain(pixels)
    #light_trail(10, red, (255, 0, 255), off, 2)
    #solid_fade([255, 0, 255], 15, 25, 100)