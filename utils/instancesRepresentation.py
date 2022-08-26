from abc import abstractmethod
from dataclasses import dataclass
from typing import Text
import numpy as np

@dataclass
class OptimizationInstance():
    solution: np.array

    @abstractmethod
    def objective(self, solution = None, isMinimizing = True) -> float:
        return NotImplemented

@dataclass
class KnapsackInstance(OptimizationInstance):
    numberOfItems: int = -1
    numberOfKnapsacks: int = -1
    itemsProfits: np.array = np.array([])
    itemsWeights: np.array = np.array([])
    knapsacksCapacities: np.array = np.array([])
    noFeasibleSolutionPenalty: int = -1
    solution: np.array = np.array([])

    def __assertIsInitialized__(self):
        assert self.numberOfItems > 0
        assert self.numberOfKnapsacks > 0
        assert self.itemsProfits.size > 0
        assert self.itemsWeights.size > 0
        assert self.knapsacksCapacities.size > 0
        assert self.noFeasibleSolutionPenalty > 0
        
    def __assertHasSolution__(self):
        assert self.solution.size > 0        

    def objective(self, solution = None, isMinimizing = True) -> int:
        self.__assertIsInitialized__()

        # Calculate the FO for self.solution
        if solution is None:
            self.__assertHasSolution__()
            solution = self.solution

        # Calculate the FO for the solution passed as an argument
        else: 
            solution = solution

        numberOfItems = self.numberOfItems
        numberOfKnapsacks = self.numberOfKnapsacks
        itemsProfits = self.itemsProfits
        itemsWeights = self.itemsWeights
        knapsacksCapacities = self.knapsacksCapacities
        noFeasiblePenalty = self.noFeasibleSolutionPenalty

        foValue = 0
        totalKnapsacksWeights = np.zeros(numberOfKnapsacks, dtype = int)
        
        for item in range(numberOfItems):
            if solution[item] != 0:
                profit = itemsProfits[item]
                weight = itemsWeights[item]
                knapsack = solution[item] - 1
                foValue += profit
                totalKnapsacksWeights[knapsack] += weight

        for knapsack in range(numberOfKnapsacks):
            if totalKnapsacksWeights[knapsack] > knapsacksCapacities[knapsack]:
                foValue -= noFeasiblePenalty * (totalKnapsacksWeights[knapsack] - knapsacksCapacities[knapsack])
        
        if isMinimizing:
            return -foValue

        return foValue

    def calculateKnapsacksWeights(self, solution = None) -> np.array:
        self.__assertIsInitialized__()
        
        # Calculate the knapsacks weights for self.solution
        if solution is None:
            self.__assertHasSolution__()
            solution = self.solution

        # Calculate the knapsacks weights for the solution passed as an argument
        else: 
            solution = solution

        solution = self.solution
        numberOfItems = self.numberOfItems
        numberOfKnapsacks = self.numberOfKnapsacks
        itemsWeights = self.itemsWeights

        knapsacksWeights = np.zeros(numberOfKnapsacks, dtype = int)

        for item in range(numberOfItems):
            knapsackIndex = solution[item] - 1
            if knapsackIndex >= 0:
                itemWeight = itemsWeights[item]
                knapsacksWeights[knapsackIndex] += itemWeight
        
        return knapsacksWeights

    def loadInstanceFromFile(self, datapath: Text):
        with open(datapath) as f:
            self.numberOfItems, self.numberOfKnapsacks = [int(v) for v in f.readline().strip().split()]

            self.itemsProfits = np.array([int(profit) for profit in f.readline().strip().split()], dtype = int)
            self.itemsWeights = np.array([int(weight) for weight in f.readline().strip().split()], dtype = int)

            self.knapsacksCapacities = np.array([int(capacity) for capacity in f.readline().strip().split()], dtype = int)

        # Penalty for infeasible solutions
        self.noFeasibleSolutionPenalty = self.itemsProfits.sum()

    def updateSolution(self, newSolution: np.array):
        self.solution = newSolution