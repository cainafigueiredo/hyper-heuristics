from typing import Callable

import copy

from utils.instancesRepresentation import OptimizationInstance
from utils.knapsackSortFunctions import sortIndexesByProfitWeightDensity

def getRandomRepairOperator(**kwargs):
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

def getGreedyRepairOperator(sortIndexesFunction: Callable = sortIndexesByProfitWeightDensity, **kwargs):
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