import time
import copy

from src.HyperHeuristic import State

from .LocalSearch import LocalSearch 

class BestImprovement(LocalSearch):
    def __init__(self):
        pass
    
    def iterate(self, instance: State, randomState: int = 0):
        solution = copy.deepcopy(instance.solution)

        numberOfItems = instance.numberOfItems
        numberOfKnapsacks = instance.numberOfKnapsacks

        startTime = time.time() 
        foundTime =time.time()

        while 1:   
            bestSolutionFOValue = instance.objective(solution, isMinimizing = False)

            bestItem = -1
            bestKnapsack = -1
            
            for i in range(numberOfItems):
                currentKnapsack = solution[i]
                for j in range(numberOfKnapsacks):
                    solution[i] = j
                    currentFOValue = instance.objective(solution, isMinimizing = False)
                    if currentFOValue > bestSolutionFOValue:
                        bestItem = i
                        bestKnapsack = j
                        bestSolutionFOValue = currentFOValue
                    
                solution[i] = currentKnapsack
            
            if bestItem != -1:
                solution[bestItem] = bestKnapsack
                foundTime = time.time()
            else:
                break 
        
        instance.solution = solution

        timeToFindSolution = foundTime - startTime

        return instance