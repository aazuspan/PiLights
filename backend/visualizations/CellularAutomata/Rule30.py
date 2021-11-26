from backend.visualizations.CellularAutomata.WolframRule import WolframRule
from backend import constants
from backend import utils

import copy
import random
import time

class Rule30(WolframRule):
    name = 'Rule 30'
    description = 'Wolfram rule #30.'
    hide = False

    outputs = WolframRule.rule_from_int(30)
