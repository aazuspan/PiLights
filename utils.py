import time
import constants


# TODO: Refactor this to use change_value function
def change_brightness(color, delta, minimum=constants.MIN_BRIGHTNESS, maximum=constants.MAX_BRIGHTNESS):
    """
    Change the color of a tuple within the brightness range for all bands that are not 0.
    
    :param color: List of ints in form [r, g, b], representing color to change
    :param delta: Int amount to change brightness
    :param minimum: Int minimum brightness to reduce values to
    :param maximum: Int maximum brightness to increase values to
    :return : List of ints in form [r, g, b], representing changed color
    """
    new_color = []
    
    for val in color:
        new_val = val
        
        # Avoid reducing brightness outside of bounds
        if minimum <= val + delta <= maximum and val != 0:
            new_val += delta
        elif val == 0:
            new_val = 0
        elif val + delta <= minimum:
            new_val = minimum
        elif val + delta >= maximum:
            new_val = maximum
        
        new_color.append(new_val)
    return new_color


def change_value(current_value, delta, minimum=constants.MIN_BRIGHTNESS, maximum=constants.MAX_BRIGHTNESS):
    """
    Change the value of a single pixel within the brightness range
    :param current_value: int current pixel brightness between 0 and 255
    :param delta: int amount to change value
    :param minimum: int minimum value to change value to
    :param maximum: int maximum value to change value to 
    :return : int value changed by delta
    """
    new_val = current_value
    
    # Avoid reducing brightness outside of bounds
    if minimum <= current_value + delta <= maximum and current_value != 0:
        new_val += delta
    elif current_value == 0:
        new_val = 0
    elif current_value + delta <= minimum:
        new_val = minimum
    elif current_value + delta >= maximum:
        new_val = maximum
    
    return new_val


def light_trail(pixels, trail_length, head_color, trail_color, fill_color, delay_ms=0):
    """
    Draw a trail of light with a solid head and fading trail that leaves a fill behind
    """
    brightness_delta = -int(constants.MAX_BRIGHTNESS / trail_length)

    for i in range(constants.PIXEL_COUNT):
        pixels[i] = head_color

        for j in range(1, trail_length):
            fade_color = change_brightness(trail_color, brightness_delta * j)
            pixels[i - j] = fade_color

        pixels[i - trail_length - 1] = fill_color

        time.sleep(delay_ms / 1000)
        pixels.show()


def solid_fade(pixels, color, delay_ms=0, min_brightness=constants.MIN_BRIGHTNESS, max_brightness=constants.MAX_BRIGHTNESS):
    solid_fade_up(pixels, color, delay_ms, min_brightness, max_brightness)
    solid_fade_down(pixels, color, delay_ms, min_brightness, max_brightness)


def solid_fade_up(pixels, color, delay_ms, min_brightness, max_brightness):
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
        time.sleep(delay_ms / 1000)


def solid_fade_down(pixels, color, delay_ms, min_brightness, max_brightness):
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
        time.sleep(delay_ms / 1000)