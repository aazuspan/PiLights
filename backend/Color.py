def clamp(x, min_val, max_val):
    """
    Clamp a value x between a minimum value and a maximum value.
    :param x: int value to clamp
    :param min_val: int minimum value to clamp to
    :param max_val: int maximum value to clamp to
    """
    return max(min(max_val, x), min_val)


class Color:
    def __init__(self, color, bits=8):
        self.bits = bits
        self.color = self.parse_color(color)

    def __add__(self, other):
        """
        Add a value or color to the color, creating a new color that combines the
        pixel values.
        :param other: int, list, tuple, or Color to add to the Color.
        """
        if type(other) in [list, tuple]:
            other = Color(other)
        elif type(other) == int:
            other = Color((other, other, other))
        if type(other) == Color:
            return Color((self.r + other.r, self.g + other.g, self.b + other.b))
        
        else:
            raise TypeError('Can only add Color, int, tuple, or list to Color.')
    
    def __sub__(self, other):
        """
        Subtract a value or color to the color, creating a new color that combines the
        pixel values.
        :param other: int, list, tuple, or Color to subtract from the Color.
        """
        if type(other) in [list, tuple]:
            other = Color(other)
        elif type(other) == int:
            other = Color((other, other, other))
        if type(other) == Color:
            return Color((self.r - other.r, self.g - other.g, self.b - other.b))

        else:
            raise TypeError('Can only subtract Color, int, tuple, or list to Color.')

    
    @property
    def minimum(self):
        """
        Minimum pixel value represented in this color 
        """
        return 0
    
    @property
    def maximum(self):
        """
        Maximum pixel value represented in this color
        """
        return 2 ** self.bits - 1
        
    @property
    def r(self):
        return self.color[0]
    
    @property
    def g(self):
        return self.color[1]
    
    @property
    def b(self):
        return self.color[2]
        
    def clamp_value(self, value):
        """
        Clamp a single color value to the value range of this color
        """
        return clamp(value, self.minimum, self.maximum)
        
    def parse_color(self, color):
        """
        Parse a color input, converting it into form (r, g, b) and clamping all values within
        usable color range for this Color.
        
        :param color: int, tuple, or list representing a color. An int will be considered
        the same value for all 3 bands. A tuple or list must be length of 3, representing
        all 3 bands.
        :return : tuple (r, g, b)
        """
        parsed = None
        
        if type(color) == int:
            value = self.clamp_value(color)
            parsed = (color, color, color)
            
        elif type(color) in [tuple, list]:
            if len(color) != 3:
                raise AttributeError('Colors must contain 3 values representing red, green, and blue.')
            else:
                r = self.clamp_value(color[0])
                g = self.clamp_value(color[1])
                b = self.clamp_value(color[2])
                
                parsed = (r, g, b)
        
        else:
            raise AttributeError('Color must be integer, tuple, or list.')
            
        return parsed
