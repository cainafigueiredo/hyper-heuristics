from typing import Callable

import copy
import numpy as np

from utils.instancesRepresentation import OptimizationInstance
from utils.knapsackSortFunctions import sortIndexesByProfitWeightDensity

def getRandomRemoveOperator(destroyRate: float, **kwargs) -> Callable:
    def randomRemove(instance: OptimizationInstance, randomState: int = 0):
        copyInstance = copy.deepcopy(instance)

        numberOfItems = instance.numberOfItems

        numberOfItemToRemove = int(numberOfItems*destroyRate)
        itemsToRemove = randomState.choice(
            np.arange(numberOfItems), 
            replace = False,
            size = numberOfItemToRemove
        ) 

        for itemToRemove in itemsToRemove:
            copyInstance.solution[itemToRemove] = 0

        return copyInstance

    return randomRemove

def getWorstRemoveOperator(destroyRate: float, sortIndexesFunction: Callable = sortIndexesByProfitWeightDensity, **kwargs) -> Callable:
    def worstRemove(instance: OptimizationInstance, randomState: int = 0):        
        copyInstance = copy.deepcopy(instance)

        numberOfItems = instance.numberOfItems

        numberOfItemsToRemove = int(numberOfItems*destroyRate)

        orderedIndexes = sortIndexesFunction(instance)[::-1] # The order should be from the best to the worst
        itemsToRemove = orderedIndexes[:numberOfItemsToRemove]

        for itemToRemove in itemsToRemove:
            copyInstance.solution[itemToRemove] = 0

        return copyInstance

    return worstRemove