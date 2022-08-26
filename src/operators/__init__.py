from typing import Callable

import copy
import numpy as np

from utils.instancesRepresentation import OptimizationInstance
from utils.knapsackSortFunctions import sortIndexesByProfitWeightDensity

def getRandomRemoveOperator(destroyRate: float) -> Callable:
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

def getWorstRemoveOperator(destroyRate: float, sortIndexesFunction: Callable = sortIndexesByProfitWeightDensity) -> Callable:
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

def getRandomRepairOperator():
    def randomRepair(instance: OptimizationInstance, randomState: int = 0):
        copyInstance = copy.deepcopy(instance)

        numberOfKnapsacks = instance.numberOfKnapsacks
        itemsWeights = instance.itemsWeights
        knapsacksCapacities = instance.knapsacksCapacities
        knapsacksWeights = instance.calculateKnapsacksWeights(copyInstance.solution)

        unselectedItems = [i for i, sol in enumerate(copyInstance.solution) if sol == 0]
        availableKnapsacks = list(range(numberOfKnapsacks))

        while unselectedItems != []:
            randomState.shuffle(unselectedItems)
            randomState.shuffle(availableKnapsacks)
            sortedItem = unselectedItems.pop()

            while availableKnapsacks != []:
                sortedKnapsack = availableKnapsacks.pop()
                
                canInsert = itemsWeights[sortedItem] + knapsacksWeights[sortedKnapsack] <= knapsacksCapacities[sortedKnapsack]

                if canInsert:
                    copyInstance.solution[sortedItem] = sortedKnapsack + 1
                    knapsacksWeights[sortedKnapsack] += itemsWeights[sortedItem]

            availableKnapsacks = list(range(numberOfKnapsacks))
    

        return copyInstance

    return randomRepair

def getGreedyRepairOperator(sortIndexesFunction: Callable = sortIndexesByProfitWeightDensity):
    def greedyRepair(instance: OptimizationInstance, randomState: int = 0):
        copyInstance = copy.deepcopy(instance)

        numberOfKnapsacks = instance.numberOfKnapsacks
        itemsWeights = instance.itemsWeights
        knapsacksCapacities = instance.knapsacksCapacities
        knapsacksWeights = instance.calculateKnapsacksWeights(copyInstance.solution)

        orderedIndexes = sortIndexesFunction(instance)

        unselectedItems = [i for i in orderedIndexes if copyInstance.solution[i] == 0]
        availableKnapsacks = list(range(numberOfKnapsacks))

        while unselectedItems != []:
            randomState.shuffle(availableKnapsacks)
            sortedItem = unselectedItems.pop()

            while availableKnapsacks != []:
                sortedKnapsack = availableKnapsacks.pop()

                canInsert = itemsWeights[sortedItem] + knapsacksWeights[sortedKnapsack] <= knapsacksCapacities[sortedKnapsack]

                if canInsert:
                    copyInstance.solution[sortedItem] = sortedKnapsack + 1
                    knapsacksWeights[sortedKnapsack] += itemsWeights[sortedItem]

            availableKnapsacks = list(range(numberOfKnapsacks))
    

        return copyInstance

    return greedyRepair