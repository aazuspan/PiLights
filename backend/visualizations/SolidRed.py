from backend.utils import light_trail
from backend.visualizations.Visualization import Visualization
from backend.visualizations import categories


class SolidRed(Visualization):
    name = 'Solid Red'
    description = 'Solid red light.'
    category = categories.SOLID

    def render(self):
        pass
