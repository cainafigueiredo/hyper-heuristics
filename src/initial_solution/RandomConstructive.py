from .ConstructiveHeuristic import ConstructiveHeuristic
from src import State

import numpy as np
from numpy.random import RandomState

class RandomConstructive(ConstructiveHeuristic):
    def __init__(self):
        pass

    def __call__(self, rnd: RandomState, instance: State) -> bool:
        numberOfItems = instance.numberOfItems
        numberOfKnapsacks = instance.numberOfKnapsacks

        solution = np.zeros(numberOfItems, dtype = int)
            
        for item in range(numberOfItems):
            solution[item] = rnd.randint(0, numberOfKnapsacks)

        instance.solution = solution

        return instance