import datetime

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class BinaryClock(Visualization):
    name = 'Binary Clock'
    description = 'Easily track the time with 17 rapidly flashing lights.'
    
    digit_spacing = 3
    unit_spacing = 6
    fill_color = (0, 8, 2)
    off_color = (0, 35, 10)
    on_color = (5, 255, 50)
    ms_delay = 500
    
    hour_start = 0
    minute_start = hour_start + 5 * digit_spacing + unit_spacing
    second_start = minute_start + 6 * digit_spacing + unit_spacing

    def __init__(self, pixels):
        super().__init__(pixels)
    
    def render(self):
        self.pixels.fill(self.fill_color)
        
        self.render_hours()
        self.render_minutes()
        self.render_seconds()
        
        self.pixels.show()

    def render_seconds(self):
        seconds = datetime.datetime.now().second
        binary_seconds = self.int2binary(seconds)
        
        for i, digit in enumerate(binary_seconds):
            if digit == "1":
                self.pixels[self.second_start + i * self.digit_spacing] = self.on_color
            else:
                self.pixels[self.second_start + i * self.digit_spacing] = self.off_color
    
    def render_minutes(self):
        minutes = datetime.datetime.now().minute
        binary_minutes = self.int2binary(minutes)
        
        for i, digit in enumerate(binary_minutes):
            if digit == "1":
                self.pixels[self.minute_start + i * self.digit_spacing] = self.on_color
            else:
                self.pixels[self.minute_start + i * self.digit_spacing] = self.off_color
                
    def render_hours(self):
        hours = datetime.datetime.now().hour
        binary_hours = self.int2binary(hours)
        
        for i, digit in enumerate(binary_hours):
            if digit == "1":
                self.pixels[self.hour_start + i * self.digit_spacing] = self.on_color
            else:
                self.pixels[self.hour_start + i * self.digit_spacing] = self.off_color
    
    def int2binary(self, x):
        """
        Convert an int to binary and return a string
        """
        return ("{0:b}".format(x))