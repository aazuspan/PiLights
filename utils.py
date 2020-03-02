from constants import *

def change_brightness(color, delta, minimum=MIN_BRIGHTNESS, maximum=MAX_BRIGHTNESS):
    """
    Change the color of a tuple within the brightness range for all bands that are not 0.
    
    :param color: List of ints in form [r, g, b], representing color to change
    :param delta: Int amount to change brightness
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