from backend.visualizations.Visualization import Visualization


class SolidBlue(Visualization):
    name = 'Solid Blue'
    description = 'Solid blue light.'

    def render(self):
        self.pixels.fill((0, 0, 255))
        self.pixels.show()
