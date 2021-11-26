from backend.visualizations.CellularAutomata.WolframRule import WolframRule
from backend import constants
from backend import utils

import copy
import random
import time

class Rule90(WolframRule):
    name = 'Rule 90'
    description = 'Wolfram rule #90.'
    hide = False
    
    #outputs = "01011010"
    outputs = WolframRule.rule_from_int(90)