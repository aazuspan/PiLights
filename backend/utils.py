import math
import time
from backend import constants


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
        
def remap(value, current_min, current_max, target_min, target_max):
    return (value - current_min) * (target_max - target_min) / (current_max - current_min) + target_min

def sleep_ms(seconds):
    time.sleep(seconds/1000)

def floatcolor2intcolor(float_color):
    """
    Convert a color made of floats into a color made of ints
    :param float_color : Tuple of floats (r, g, b)
    :return : Tuple of ints (r, g, b)
    """
    int_color = []
    
    for i in range(len(float_color)):
        int_color.append(int(float_color[i]))
    
    return int_color

def interpolate_value(start_value, end_value, weight):
    """
    Linearly interpolate between two colors.
    
    :param start_value : Float value to interpolate from
    :param end_value : Float value to interpolate towards
    :param weight : Float proportion of distance between start and end values to interpolate to
    :return : Float value interpolated between start and end
    """
    return start_value + weight * (end_value - start_value)
    
def interpolate_color(start_color, end_color, weight):
    """
    Linearly interpolate between two colors.
    
    :param start_color : Tuple of ints (r, g, b) color to interpolate from
    :param end_color : Tuple of ints (r, g, b) color to interpolate towards
    :param weight : Float proportion of distance between start and end values to interpolate to
    :return : Tuple of floats (r, g, b) color interpolated between start and end
    """
    interpolated_color = []
    
    for i in range(len(start_color)):
        interpolated_band = start_color[i] + weight * (end_color[i] - start_color[i])
        interpolated_color.append(interpolated_band)
    
    interpolated_color = floatcolor2intcolor(interpolated_color)
    
    return interpolated_color

def interpolate_color_from_dict(color_dictionary, x):
    """
    Given a value x within the range of the keys of a dictionary, where the values of the dictionary are
    colors, interpolate the color at location x within the dictionary.
    :param color_dictionary : Dictionary where keys are floats or ints and values are tuple RGB colors
    :param x: Float or int value to compare with dictionary keys
    """
    interp_bounds = get_interpolation_bounds(color_dictionary, x)
    interp_color = interpolate_color(interp_bounds[0], interp_bounds[1], interp_bounds[2])
    return interp_color

def get_interpolation_bounds(dictionary, x):
    """
    Given a value x within the range of the keys of a dictionary, return the values of the keys that surround that value,
    as well as the relative location of the value between those keys.

    Example:
    Determining a color range from a temperature.

    dictionary = {1000: "red", 5000: "white", 10000: "blue"}
    x = 8000
    return = ("white", "blue", 0.6)
    This means that the temperature 8000 falls 60% of the way between white and blue.


    If the value x provided is outside of the dictionary bounds, the
    nearest dictionary value will be returned.

    :param dictionary: An ordered dictionary with ints or floats as keys
    :param x: Int or float
    :return: Tuple (lower bound, upper bound, location between)
    """
    closest_index = get_closest_index(dictionary.keys(), x)
    keys = list(dictionary)
    closest_key = keys[closest_index]

    # If value is outside the bounds of the dictionary or equal to the closest value
    if (closest_index == 0 and x < closest_key) or (closest_index == len(dictionary) - 1 and x > closest_key) or x == closest_key:
        lower_bound_key = keys[closest_index]
        upper_bound_key = keys[closest_index]
        location = 1.0

    # If value is between two values in the dictionary
    else:
        if x < keys[closest_index]:
            lower_bound_key = keys[closest_index - 1]
            upper_bound_key = closest_key

        else:
            lower_bound_key = closest_key
            upper_bound_key = keys[closest_index + 1]

        location = get_location(lower_bound_key, upper_bound_key, x)

    lower_bound = dictionary[lower_bound_key]
    upper_bound = dictionary[upper_bound_key]

    return lower_bound, upper_bound, location


def get_closest_index(array, x):
    """
    Find the index of the value in the array closest to x
    :param array: Array of ints or floats
    :param x: Number
    :return: int index of the closest value in the array
    """
    closest = None
    closest_diff = math.inf

    for i, val in enumerate(array):
        diff = abs(x - val)
        if diff < closest_diff:
            closest = i
            closest_diff = diff

    return closest


def get_location(lower, upper, x):
    """
    Get the location of a value x between a lower and upper bound, from 0 to 1. For example, the location of 5 between
    0 and 10 is 0.5. The location of 90 between 0 and 100 is 0.9.
    :param lower: Float lower bound
    :param upper: Float upper bound
    :param x: Value between lower and upper
    :return: Float location between lower and upper bounds
    """
    return (x - lower) / (upper - lower)

def floatcolor2intcolor(floatcolor):
    """
    Convert a tuple of floats to a list of ints. Use this to ensure colors are ints, as floats are
    not valid inputs for Neopixel.
    :param floatcolor: A tuple of floats, representing the bands of a color
    :return : A list of ints, representing the bands of a color
    """
    intcolor = []
    for band in floatcolor:
        intband = int(band)
        if intband < 0:
            intband = 0
        if intband > 255:
            intband = 255
        intcolor.append(intband)
        
    return intcolor


def pixel_is_out_of_bounds(i):
    """
    Check if a pixel index is out of the pixel bounds
    """
    if i < 0 or i >= constants.PIXEL_COUNT - 1:
        return True
    return False


def wraparound(i):
    """
    Get the pixel index wrapped around the strip. For example, pixel 110 in a string of 100 pixels
    would return 10
    """
    while i < 0:
        i += constants.PIXEL_COUNT
            
    while i >= constants.PIXEL_COUNT:
        i -= constants.PIXEL_COUNT
    
    return i


def int2binary(x):
    """
    Convert an int to binary and return a string
    """
    return ("{0:b}".format(x))
