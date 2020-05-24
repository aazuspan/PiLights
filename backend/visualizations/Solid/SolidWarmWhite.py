from backend.visualizations.Visualization import Visualization


class SolidWarmWhite(Visualization):
    name = 'Solid Warm White'
    description = 'Solid warm white light.'

    def render(self):
        self.pixels.fill((255, 225, 200))
        self.pixels.show()
