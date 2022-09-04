from typing import Callable

import copy

from src.HyperHeuristic import State
from utils.knapsackSortFunctions import sortIndexesByProfitWeightDensity

from .Operator import RepairOperator

class RandomRepair(RepairOperator):
    def __init__(self):
        pass

    def iterate(self, instance: State, randomState: int = 0):
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

class GreedyRepair(RepairOperator):
    def __init__(self, sortIndexesFunction: Callable = sortIndexesByProfitWeightDensity):
        self.sortIndexesFunction = sortIndexesFunction
        
    def iterate(self, instance: State, randomState: int = 0):
        copyInstance = copy.deepcopy(instance)

        numberOfKnapsacks = instance.numberOfKnapsacks
        itemsWeights = instance.itemsWeights
        knapsacksCapacities = instance.knapsacksCapacities
        knapsacksWeights = instance.calculateKnapsacksWeights(copyInstance.solution)

        orderedIndexes = self.sortIndexesFunction(instance)

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

class RegretInsertion(RepairOperator):
    def __init__(self):
        pass

    def iterate(self, instance: State, randomState: int = 0):
        copyInstance = copy.deepcopy(instance)
        solution = copyInstance.solution

        numberOfKnapsacks = copyInstance.numberOfKnapsacks

        vetDifFO=[0]*len(solution)
        vetBestMoc=[0]*len(solution)
        
        FO=copyInstance.objective(solution)
        
        for i in range(len(solution)):
            firtsBestFO=FO
            secondBestFO=FO
            firtsMoch=0
            secondMoch=0
            parcFO=0
        
            if solution[i]==0:
                for j in range(numberOfKnapsacks):
                    solution[i]=j+1
                    parcFO=copyInstance.objective(solution)

                    if parcFO>=firtsBestFO:
                        secondBestFO=firtsBestFO
                        firtsBestFO=parcFO
                        secondMoch=firtsMoch
                        firtsMoch=j+1
                        vetDifFO[i]=secondBestFO-FO
                        vetBestMoc[i]=secondMoch
                    solution[i]=0
                    
        idx=vetDifFO.index(max(vetDifFO))
        solution[idx]=vetBestMoc[idx]
        
        return copyInstance