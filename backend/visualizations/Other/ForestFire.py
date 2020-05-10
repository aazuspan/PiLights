import random

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class ForestFire(Visualization):
    name = 'Forest Fire'
    description = 'Green trees grow and then burn orange.'

    initial_density = 0.1
    
    fire_temp = {
        0: (15, 0, 0),
        200: (20, 5, 0),
        400: (25, 10, 0),
        500: (50, 15, 0),
        700: (75, 20, 0),
        800: (100, 25, 5),
        900: (150, 50, 10),
        1000: (200, 75, 15),
        1100: (225, 115, 20),
        1200: (255, 135, 25),
        1300: (255, 150, 50),
        1400: (255, 175, 60),
        1500: (255, 200, 75),
    }
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.forest = self.generate_forest()

    def render(self):
        self.pixels.fill((0, 0, 0))
        for cell in self.forest:
            if cell:
                cell.grow()
                cell.render()
                
        self.pixels.show()
        utils.sleep_ms(0)
        
    def generate_forest(self):
        """
        Initialize and the forest by randomly generating trees
        """
        forest = []
        for i in range(constants.PIXEL_COUNT):
            if random.random() < self.initial_density:
                cell = Tree(self, i)
            else:
                cell = None
            forest.append(cell)
        return forest

class Tree:
    seed_viability_rate = 0.1
    burn_rate = 0.001
    reproductive_age = 20
    max_burn_rounds = 50
    catch_rounds = 25
    catch_rate = 0.1
    
    def __init__(self, forest, index):
        self.forest = forest
        self.index = index
        self.age = 0
        self.burning = False
        self.burn_rounds = 0
    
    @property
    def color(self):
        if not self.burning:
            color = utils.floatcolor2intcolor((0, min(255, self.age), 0))
        else:
            color = (255, 150, 0)
            
        return color
    
    def grow(self):
        if self.burning:
            self.burn()
            
        else:
            self.chance_to_burn()
            self.age += 1
            if self.age > self.reproductive_age:
                self.release_seeds()
    
    def render(self):
        self.forest.pixels[self.index] = self.color
    
    def release_seeds(self):
        try:
            if random.random() < self.seed_viability_rate:
                direction = random.choice([-1, 1])
                if not self.forest.forest[self.index + direction]:
                    self.forest.forest[self.index + direction] = Tree(self.forest, self.index + direction)
        except IndexError:
            pass
    
    def chance_to_burn(self):
        if random.random() < self.burn_rate:
            self.burning = True
            self.burn()
    
    def burn(self):
        if self.burn_rounds >= self.max_burn_rounds:
            self.die()
            
        elif self.burn_rounds >= self.catch_rounds:
            if random.random() < self.catch_rate:
                self.catch_neighbours()

        self.burn_rounds += 1
            
    
    def catch_neighbours(self):
        for offset in [-1, 1]:
            try:
                neighbour_cell = self.forest.forest[self.index + offset]
                if neighbour_cell:
                    neighbour_cell.burning = True
            except IndexError:
                pass
                
    def die(self):
        self.forest.forest[self.index] = None
