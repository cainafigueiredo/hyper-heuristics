
import copy
import time
from src.State import State

class LocalSearch:
    def __init__(self):
        pass

    def __call__(self):
        pass

class FirstImprovement(LocalSearch):
    def __init__(self):
        pass
    
    def __call__(self, instance: State, randomState: int = 0):
        solution = copy.deepcopy(instance.solution)

        numberOfItems = instance.numberOfItems
        numberOfKnapsacks = instance.numberOfKnapsacks

        while 1:
            bestSolutionFOValue = instance.objective(solution, isMinimizing = False)
            improved = False
            
            for i in range(numberOfItems):
                currentKnapsack = solution[i]
                for j in range(1, numberOfKnapsacks + 1):
                    solution[i] = j
                    currentSolutionFOValue = instance.objective(solution, isMinimizing = False)
                    # print("i", i, "totalWeight", instance.calculateKnapsacksWeights(solution), "j", j, "Current:",currentSolutionFOValue, "| Best:", bestSolutionFOValue)
                    if currentSolutionFOValue > bestSolutionFOValue:
                        improved = True
                        bestSolutionFOValue = currentSolutionFOValue
                        # print("Changed:",bestSolutionFOValue, currentSolutionFOValue)
                        break
                
                if improved:
                    break
                else:
                    solution[i] = currentKnapsack 
            
            if not improved:
                break
        
        instance.solution = solution

        return instance

class BestImprovement(LocalSearch):
    def __init__(self):
        pass
    
    def __call__(self, instance: State, randomState: int = 0):
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