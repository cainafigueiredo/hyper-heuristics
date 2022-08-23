from typing import List, Text
import numpy as np
from abc import ABC, abstractmethod

class OptimizationProblemInstance(ABC):
    def __init__(self, c: List, A: List[List], b: List):
        # """
        #     Representation of an optimization problem formulated as follows:
        #     min c^T*x
        #     s.a. Ax <= b
        #     x_i >= 0, for all i
        # """
        # self.numberOfVariables = len(c)
        # self.numberOfRestrictions = len(b)
        # self.c = np.array(c)
        # self.b = np.array(b)
        # self.A = np.array(A)
        pass

    @abstractmethod
    def calculateObjectiveFunction(self, solution, noFeasiblePenalty: int = 10):
        foValue = np.dot(self.c, solution) 
        restrictionsViolationVector = self.A.dot(solution) - self.b
        
        foValue -= noFeasiblePenalty*restrictionsViolationVector.sum()

        return foValue

    def getNumberOfVariables(self):
        return self.numberOfVariables

    def getNumberOfRestrictions(self):
        return self.numberOfRestrictions

class Knapsack(OptimizationProblemInstance):
    def __init__(self, itemsProfits = None, itemsWeights = None, knapsacksCapacities = None):
        super().__init__(itemsProfits, itemsWeights, knapsacksCapacities)

    def getNumberOfItems(self):
        self.getNumberOfVariables()

    def getNumberOfKnapsacks(self):
        return self.getNumberOfRestrictions()
    
    def getItemsProfits(self):
        return self.c

    def getItemsWeights(self):
        return self.A

    def loadFromFile(self, filepath: Text):
        with open(filepath) as f:
            nItems, nKnapsacks = f.readline().strip().split()
            itemsProfits = f.readline().strip.split()
            itemsWeights = f.readline().strip.split()
            knapsacksCapacities = f.readline().strip.split()

            self.numberOfVariables = nItems
            self.numberOfKnapsacks = nKnapsacks
            self.c = itemsProfits
            self.b = knapsacksCapacities
            self.A = itemsWeights