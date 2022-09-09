from src.State import State
from typing import Text
import numpy as np

class KnapsackInstance(State):
    def __init__(
        self, 
        numberOfItems = None,
        numberOfKnapsacks = None,
        itemsProfits = None,
        itemsWeights = None,
        knapsacksCapacities = None,
        solution = None
    ):
        self.numberOfItems = numberOfItems
        self.numberOfKnapsacks = numberOfKnapsacks
        self.itemsProfits = itemsProfits
        self.itemsWeights = itemsWeights
        self.knapsacksCapacities = knapsacksCapacities
        self.noFeasibleSolutionPenalty = self.itemsProfits.sum() if not self.itemsProfits is None else None
        self.solution = solution

    def __assertIsInitialized__(self):
        assert self.numberOfItems > 0
        assert self.numberOfKnapsacks > 0
        assert self.itemsProfits.size > 0
        assert self.itemsWeights.size > 0
        assert self.knapsacksCapacities.size > 0
        
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
                # Sometimes, overflow induces to a inversion of sign (negative -> positive)
                # We assign it as -inf when it occurs
                if foValue > 0:
                    foValue = -np.inf
                    break

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