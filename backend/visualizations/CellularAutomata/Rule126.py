from backend.visualizations.CellularAutomata.WolframRule import WolframRule
from backend import constants
from backend import utils

import copy
import random
import time

class Rule126(WolframRule):
    name = 'Rule 126'
    description = 'Wolfram rule #126.'
    hide = False
    
    outputs = WolframRule.rule_from_int(126)