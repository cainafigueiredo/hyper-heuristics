import copy
from src.HyperHeuristic import State
from .LocalSearch import LocalSearch 

class FirstImprovement(LocalSearch):
    def __init__(self):
        pass
    
    def iterate(self, instance: State, randomState: int = 0):
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