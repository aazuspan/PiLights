import random

from backend import utils, constants
from backend.visualizations.Visualization import Visualization


class ForestFire(Visualization):
    name = 'Forest Fire'
    description = 'Green trees grow and then burn orange.'

    initial_density = 0.1
    sprout_chance = 0.0001
    
    def __init__(self, pixels):
        super().__init__(pixels)
        self.forest = self.generate_forest()

    #TODO: Add random chance to spawn new trees (sprouting)
    def render(self):
        self.pixels.fill((0, 0, 0))
        self.chance_to_sprout()
        for cell in self.forest:
            if cell:
                cell.grow()
                cell.render()
                
        self.pixels.show()
        
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

    def chance_to_sprout(self):
        """
        Chance to sprout a new tree
        """
        for i in range(constants.PIXEL_COUNT):
            if not self.forest[i]:
                if random.random() < self.sprout_chance:
                    self.forest[i] = Tree(self, i)
        

class Tree:
    burn_colors = {
        0: (150, 255, 0),
        17: (200, 225, 0),
        34: (225, 200, 0),
        51: (255, 150, 0),
        68: (255, 100, 0),
        85: (255, 80, 0),
        102: (255, 60, 0),
        119: (225, 40, 0),
        136: (175, 25, 0),
        153: (125, 20, 0),
        170: (100, 15, 0),
        187: (75, 10, 0),
        204: (35, 5, 0),
        221: (5, 0, 0),
        255: (0, 0, 0),
    }
    
    seed_viability_rate = 0.01
    burn_rate = 0.00002
    reproductive_age = 20
    minimum_burn_age = 100
    max_burn_rounds = 250
    catch_rounds = 25
    catch_rate = 1.1
    age_rate = 0.2
    
    def __init__(self, forest, index):
        self.forest = forest
        self.index = index
        self.age = 0
        self.burning = False
        self.burn_rounds = 0
    
    @property
    def color(self):
        if not self.burning:
            color = utils.floatcolor2intcolor((0, min(255, self.age), min(40, int(self.age/6))))
        else:
            color = utils.interpolate_color_from_dict(self.burn_colors, self.burn_rounds)
            
        return color
    
    def grow(self):
        if self.burning:
            self.burn()
            
        else:
            self.chance_to_burn()
            self.age += self.age_rate
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
        if self.age > self.minimum_burn_age:
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
        
