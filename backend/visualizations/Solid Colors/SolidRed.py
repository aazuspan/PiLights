from backend.visualizations.Visualization import Visualization


class SolidRed(Visualization):
    name = 'Solid Red'
    description = 'Solid red light.'

    def render(self):
        self.pixels.fill((255, 0, 0))
        self.pixels.show()
