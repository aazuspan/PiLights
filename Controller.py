import importlib
import pkgutil

import constants
from visualizations.Visualization import Visualization


class Controller:
    def get_visualizations(self):
        for (module_loader, name, ispkg) in pkgutil.iter_modules([constants.VIS_DIR]):
            importlib.import_module('visualizations.' + name, __package__)

        return Visualization.__subclasses__()


cont = Controller()
visualizations = cont.get_visualizations()
for vis in visualizations:
    print(f'{vis.name}: {vis.description}')
