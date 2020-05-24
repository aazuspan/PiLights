from backend.visualizations.Visualization import Visualization


class SolidCoolWhite(Visualization):
    name = 'Solid Cool White'
    description = 'Solid cool white light.'

    def render(self):
        self.pixels.fill((190, 200, 255))
        self.pixels.show()
