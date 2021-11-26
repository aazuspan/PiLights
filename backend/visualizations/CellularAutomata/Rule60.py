from backend.visualizations.CellularAutomata.WolframRule import WolframRule
from backend import constants
from backend import utils

import copy
import random
import time

class Rule60(WolframRule):
    name = 'Rule 60'
    description = 'Wolfram rule #60.'
    hide = False
    
    outputs = WolframRule.rule_from_int(60)
    start_position = 0