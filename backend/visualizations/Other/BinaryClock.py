import datetime

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class BinaryClock(Visualization):
    name = 'Binary Clock'
    description = 'Easily track the time with 17 rapidly flashing lights.'
    
    background_colors = {
        0: (10, 4, 12),
        6: (12, 6, 8),
        12: (15, 9, 3),
        18: (12, 7, 6),
        24: (10, 4, 12)
    }
    
    digit_spacing = 3
    unit_spacing = 5
    off_color = (50, 20, 0)
    on_color = (5, 255, 50)
    ms_delay = 500
    
    # Start indexes for each set of digits
    hour_start = 0
    minute_start = hour_start + 5 * digit_spacing + unit_spacing
    second_start = minute_start + 6 * digit_spacing + unit_spacing

    def __init__(self, pixels):
        super().__init__(pixels)
    
    def render(self):
        self.render_background()
        self.render_hours()
        self.render_minutes()
        self.render_seconds()
        
        self.pixels.show()

    def render_background(self):
        hours = datetime.datetime.now().hour
        minutes = datetime.datetime.now().minute
        time = hours + minutes/60
        interp_bounds = utils.get_interpolation_bounds(self.background_colors, time)
        interp_color = utils.interpolate_color(interp_bounds[0], interp_bounds[1], interp_bounds[2])
        self.pixels.fill(interp_color)
    
    def render_seconds(self):
        seconds = datetime.datetime.now().second
        binary_seconds = utils.int2binary(seconds)
        binary_seconds = self.add_leading_zeros(binary_seconds, len(utils.int2binary(59)))
        
        for i, digit in enumerate(binary_seconds):
            if digit == "1":
                self.pixels[self.second_start + i * self.digit_spacing] = self.on_color
            else:
                self.pixels[self.second_start + i * self.digit_spacing] = self.off_color
    
    def render_minutes(self):
        minutes = datetime.datetime.now().minute
        binary_minutes = utils.int2binary(minutes)
        binary_minutes = self.add_leading_zeros(binary_minutes, len(utils.int2binary(59)))
        
        for i, digit in enumerate(binary_minutes):
            if digit == "1":
                self.pixels[self.minute_start + i * self.digit_spacing] = self.on_color
            else:
                self.pixels[self.minute_start + i * self.digit_spacing] = self.off_color
                
    def render_hours(self):
        hours = datetime.datetime.now().hour
        binary_hours = utils.int2binary(hours)
        binary_hours = self.add_leading_zeros(binary_hours, len(utils.int2binary(23)))
        
        for i, digit in enumerate(binary_hours):
            if digit == "1":
                self.pixels[self.hour_start + i * self.digit_spacing] = self.on_color
            else:
                self.pixels[self.hour_start + i * self.digit_spacing] = self.off_color
    
    def add_leading_zeros(self, string, length):
        """
        Take a string and add leading zeros until it reaches a given length
        """
        modified_string = string
        
        while len(modified_string) < length:
            modified_string = '0' + modified_string
            
        return modified_string
