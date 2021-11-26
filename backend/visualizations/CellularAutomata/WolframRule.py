from backend.visualizations.Visualization import Visualization
from backend import constants
from backend import utils

import copy
import random
import time

class WolframRule(Visualization):
    name = 'Wolfram Rule'
    description = 'Generic Wolfram cellular automaton.'
    
    hide = True
    
    max_fade = 3
    on_color = (0, 255, 255)
    dead_color = (0, 150, 50)
    off_color = (0, 0, 0)
    
    inputs = ("111", "110", "101", "100", "011", "010", "001", "000")
    outputs = "00111100"
    
    start_position = None
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.current_cells = [0 for i in range(constants.PIXEL_COUNT)]
        self.next_cells = [0 for i in range(constants.PIXEL_COUNT)]
        self.fade_count = [self.max_fade for i in range(constants.PIXEL_COUNT)]
  
        # Seed a live cell
        start = random.randint(0, constants.PIXEL_COUNT - 1) if self.start_position == None else self.start_position
        self.current_cells[start] = 1
    
    def rule(self, l, c, r):
        """Apply a logical rule to generate a new output from a left, center, and right input.
        To simplify the implementation of new rules, this is done by simple pattern matching,
        comparing each possible input (self.inputs) to the expected outputs (self.outputs).
        
        There are more performant ways to handle this, but output strings are always available
        for rules whereas the actual logical rules are harder to find.
        """
        in_code = str(l) + str(c) + str(r)
        match = self.inputs.index(in_code)
        return int(self.outputs[match])
        
        
    def update(self):
        for i, cell in enumerate(self.current_cells):
            l = self.current_cells[i-1]
            c = cell
            r = self.current_cells[i+1] if i + 1 < len(self.current_cells) else self.current_cells[0]
            
            next_state = self.rule(l, c, r)
            self.next_cells[i] = next_state
            
            # Fade dead cells
            if not next_state:
                self.fade_count[i] = min(self.max_fade, self.fade_count[i] + 1)
            else:
                self.fade_count[i] = 0
        
        self.current_cells = copy.copy(self.next_cells)
        
    def render(self):
        for i, cell in enumerate(self.current_cells):
            fade_color = utils.interpolate_color(self.dead_color, self.off_color, self.fade_count[i]/self.max_fade)
            self.pixels[i] = fade_color if not cell else self.on_color
            
        self.pixels.show()
        self.update()
        # TODO: Replace this with a timer
        time.sleep(0.1)

    @classmethod
    def rule_from_int(cls, x):
        """Generate binary rule outputs from an integer input"""
        return f"{x:b}".zfill(8)