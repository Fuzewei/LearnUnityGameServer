# -*- coding: utf-8 -*-
import math
import Math
import random

def RandonChoice(choiceList, weight):
    assert(len(choiceList) == len(weight))
    pos = random.uniform(0, sum(weight))
    for w, value in zip(weight, choiceList):
        pos -= w
        if pos <= 0:
            return value
    assert(False, pos, total)