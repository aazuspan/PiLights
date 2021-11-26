from backend.visualizations.CellularAutomata.WolframRule import WolframRule
from backend import constants
from backend import utils

import copy
import random
import time

class Rule150(WolframRule):
    name = 'Rule 150'
    description = 'Wolfram rule #150.'
    hide = False
    
    outputs = WolframRule.rule_from_int(150)