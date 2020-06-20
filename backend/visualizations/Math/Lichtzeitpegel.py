import datetime

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class Lichtzeitpegel(Visualization):
    name = 'Lichtzeitpegel'
    description = 'A 24-hour, decimal clock (HH MM SS).'
    
    digit_spacing = 2
    place_spacing = 4
    unit_spacing = 8
    
    fill_color = (0, 0, 0)
    on_color = (5, 255, 50)
    
    hour_tens_digits = 2
    hour_ones_digits = 9
    
    minute_tens_digits = 5
    minute_ones_digits = 9
    
    second_tens_digits = 5
    second_ones_digits = 9
    
    # Start indexes for each set of digits
    hour_tens_start = 0
    hour_ones_start = hour_tens_start + hour_tens_digits * digit_spacing + place_spacing
    
    minute_tens_start = hour_ones_start + hour_ones_digits * digit_spacing + unit_spacing
    minute_ones_start = minute_tens_start + minute_tens_digits * digit_spacing + place_spacing
    
    second_tens_start = minute_ones_start + minute_ones_digits * digit_spacing + unit_spacing
    second_ones_start = second_tens_start + second_tens_digits * digit_spacing + place_spacing

    def __init__(self, pixels):
        super().__init__(pixels)
    
    def render(self):
        self.render_background()
        self.render_hours()
        self.render_minutes()
        self.render_seconds()
        
        self.pixels.show()

    def render_background(self):
        self.pixels.fill(self.fill_color)
    
    def render_number(self, number, max_number, start_index):
        """
        Render a number by splitting it into constituent digits and lighting LEDs to represent each digit.
        Example: rendering 59 will turn on 5 LEDs, create a space, and turn on 9 more LEDs.
        :param number: The number to render
        :param max_number: The maximum number that can be rendered. This is used to space LEDs.
        :param start_index: The pixel index to start rendering the number.
        """
        digits = len(str(max_number))
        digit_str = self.add_leading_zeros(str(number), digits)
        prev_digit_length = 0
        
        for digit in range(digits):
            max_leds = int(str(max_number)[digit])
            
            digit_value = int(digit_str[digit])
            digit_length = max_leds * self.digit_spacing
            digit_start = start_index + prev_digit_length + digit_length + (digit * self.place_spacing)
            
            for led in range(digit_value):
                led_index = (digit_start + digits * self.digit_spacing) - (led * self.digit_spacing)
                self.pixels[led_index] = self.on_color
            
            prev_digit_length = digit_length
    
    def render_seconds(self):
        seconds = datetime.datetime.now().second
        self.render_number(seconds, 59, self.second_tens_start)
    
    def render_minutes(self):
        minutes = datetime.datetime.now().minute
        self.render_number(minutes, 59, self.minute_tens_start)
        
    def render_hours(self):
        hours = datetime.datetime.now().hour
        self.render_number(hours, 29, self.hour_tens_start)
    
    def add_leading_zeros(self, string, length):
        """
        Take a string and add leading zeros until it reaches a given length
        """
        modified_string = string
        
        while len(modified_string) < length:
            modified_string = '0' + modified_string
            
        return modified_string
