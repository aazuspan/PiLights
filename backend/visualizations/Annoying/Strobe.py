import time
import random
from backend.visualizations.Visualization import Visualization


class Strobe(Visualization):
    name = 'Strobe'
    description = 'Strobes.'

    def render(self):
        sleep_time = random.randint(25, 100)/1000
        
        self.pixels.fill((255, 255, 255))
        self.pixels.show()
        
        time.sleep(sleep_time)

        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        
        time.sleep(sleep_time)
