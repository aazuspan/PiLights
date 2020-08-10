from backend.visualizations.Visualization import Visualization


class SolidWarmWhite(Visualization):
    name = 'Solid Warm White'
    description = 'Solid warm white light.'

    def render(self):
        self.pixels.fill((255, 150, 75))
        self.pixels.show()
