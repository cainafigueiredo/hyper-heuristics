import numpy as np

from abc import ABC, abstractmethod
from typing import Callable
from src.State import State
from numpy.random import RandomState

class ConstructiveHeuristic(ABC):
    @abstractmethod
    def __call__(self, rnd: RandomState, instance: State) -> bool:
        return NotImplemented

class GreedyConstructive(ConstructiveHeuristic):
    def __init__(self, sortIndexesFunction: Callable[[State], np.array]):
        self.sortIndexesFunction = sortIndexesFunction
    
    def __call__(self, instance: State, rnd: RandomState): 
        numberOfItems = instance.numberOfItems
        numberOfKnapsacks = instance.numberOfKnapsacks
        itemsWeights = instance.itemsWeights
        knapsacksCapacities = instance.knapsacksCapacities

        solution = np.zeros(numberOfItems, dtype = int)
        totalKnapsacksCapacities = np.zeros(numberOfKnapsacks, dtype = int)
        
        orderedIndexes = self.sortIndexesFunction(instance)
        
        for i in range(numberOfItems):
            for j in range(numberOfKnapsacks):
                if (totalKnapsacksCapacities[j] + itemsWeights[orderedIndexes[i]]) <= knapsacksCapacities[j]:
                    solution[orderedIndexes[i]] = j + 1
                    totalKnapsacksCapacities[j] += itemsWeights[orderedIndexes[i]]
                    break

        instance.solution = solution

        return instance

class GreedyRandomizedConstructive(ConstructiveHeuristic):
    def __init__(self, lrc: float):
        self.lrc = lrc

    def __call__(
        self, instance: State, rnd: RandomState
    ):
        numberOfItems = instance.numberOfItems
        numberOfKnapsacks = instance.numberOfKnapsacks
        itemsProfits = instance.itemsProfits
        itemsWeights = instance.itemsWeights
        knapsacksCapacities = instance.knapsacksCapacities

        auxVector = np.zeros(numberOfItems, dtype = int)

        lrcNumberOfCandidates = int(numberOfItems * self.lrc)
        profitsVector = np.zeros(lrcNumberOfCandidates, dtype = int)
        lrcVector = np.zeros(lrcNumberOfCandidates, dtype = int)
        
        for i in range(lrcNumberOfCandidates):
            randItem = rnd.randint(0, numberOfItems)
            while auxVector[randItem] == 1: #impede o sorteio de um numero repetido
                randItem = rnd.randint(0, numberOfItems)
            
            lrcVector[i] = randItem
            profitsVector[i] = itemsProfits[randItem]
            auxVector[randItem] = 1
        
        orderedIndexesLRC = np.argsort(profitsVector)[::-1]

        solution = np.zeros(numberOfItems, dtype = int)
        vetPes = np.zeros(numberOfKnapsacks, dtype = int)
        for i in range(lrcNumberOfCandidates):
            for j in range(numberOfKnapsacks):
                if (vetPes[j] + itemsWeights[lrcVector[orderedIndexesLRC[i]]]) <= knapsacksCapacities[j]:
                    solution[lrcVector[orderedIndexesLRC[i]]] = j + 1
                    vetPes[j] = vetPes[j] + itemsWeights[lrcVector[orderedIndexesLRC[i]]]
                    break

        vAuxIndObj = np.argsort(itemsProfits)[::-1]
        for i in range(numberOfItems):
            if auxVector[vAuxIndObj[i]] == 0:
                for j in range(numberOfKnapsacks):
                    if (vetPes[j] + itemsWeights[vAuxIndObj[i]]) <= knapsacksCapacities[j]:
                        solution[vAuxIndObj[i]] = j + 1
                        vetPes[j] = vetPes[j] + itemsWeights[vAuxIndObj[i]]
                        break

        instance.solution = solution

        return instance

class RandomConstructive(ConstructiveHeuristic):
    def __init__(self):
        pass

    def __call__(self, instance: State, rnd: RandomState):
        numberOfItems = instance.numberOfItems
        numberOfKnapsacks = instance.numberOfKnapsacks

        solution = np.zeros(numberOfItems, dtype = int)
            
        for item in range(numberOfItems):
            solution[item] = rnd.randint(0, numberOfKnapsacks+1)

        instance.solution = solution

        return instance