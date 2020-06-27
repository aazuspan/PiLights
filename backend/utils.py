import math
import time
from backend import constants


# TODO: Remove this method and refactor the Rain vis to interpolate instead
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


def remap(value, current_min, current_max, target_min, target_max):
    """
    Arduino-style remap function to shift a value within a current range to a new value within a target range
    """
    return (value - current_min) * (target_max - target_min) / (current_max - current_min) + target_min


def sleep_ms(seconds):
    time.sleep(seconds/1000)


def floatcolor2intcolor(float_color):
    """
    Convert a color made of floats into a color made of ints
    :param float_color : Tuple of floats (r, g, b)
    :return : Tuple of floats (r, g, b)
    """
    int_color = []
    
    for i in range(len(float_color)):
        int_color.append(int(float_color[i]))
    
    return int_color

def get_blurred_pixels(pixel_index, center_color, edge_color=(0, 0, 0), kernel_width=3):
    """
    Interpolate colors around a pixel index to create a blurred pixel
    :param pixel_index: int index of the center pixel
    :param color: tuple of ints (r, g, b)
    :param kernel_width: int width of blurred pixels. Must be odd.
    :return : list of tuples, representing index and color of blurred pixels
    """
    
    if kernel_width % 2 == 0:
        raise AttributeError("Kernel width must be odd")
    
    half_width = int((kernel_width - 1) / 2)
    
    pixels = [(pixel_index, center_color)]
    
    for offset in range(half_width):
        for direction in (-1, 1):
            index = pixel_index + (offset + 1) * direction
            distance = 1 - (1 / (half_width + 1) * (offset + 1))
            color = interpolate_color(edge_color, center_color, distance)
            pixels.append((index, color))
    
    return pixels

def interpolate_pixels(pixel_index, color):
    """
    Interpolate colors around an intermediate pixel index. For example, if pixel index 4.8
    is set to red, pixel 4 will be set to dim red and pixel 5 will be set to brighter red.
    
    :param pixel_index: Float intermediate pixel index
    :param color: tuple of ints (r, g, b)
    :return : tuple of tuples, representing lower index and color and upper index and color
    """
    lower_index = math.floor(pixel_index)
    upper_index = math.ceil(pixel_index)
    
    lower_distance = pixel_index - lower_index
    upper_distance = upper_index - pixel_index
    
    lower_color = interpolate_color(color, (0, 0, 0), lower_distance)
    upper_color = interpolate_color(color, (0, 0, 0), upper_distance)
    
    return ((lower_index, lower_color), (upper_index, upper_color))
    
    
def interpolate_value(start_value, end_value, weight):
    """
    Linearly interpolate between two values.
    
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
        interpolated_band = interpolate_value(start_color[i], end_color[i], weight)
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


def clamp(x, min_val, max_val):
    """
    Clamp a value x betwen a minimum value and a maximum value.
    :param x: int value to clamp
    :param min_val: int minimum value to clamp to
    :param max_val: int maximum value to clamp to
    """
    return max(min(max_val, x), min_val)
