from backend.visualizations.CellularAutomata.WolframRule import WolframRule
from backend import constants
from backend import utils

import copy
import random
import time

class Rule182(WolframRule):
    name = 'Rule 182'
    description = 'Wolfram rule #182.'
    hide = False
    
    max_fade = 1
    outputs = WolframRule.rule_from_int(182)