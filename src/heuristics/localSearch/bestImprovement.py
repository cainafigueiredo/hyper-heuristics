# -*- coding: utf-8 -*-

"""
@author: Leonardo Rosas Leal, Daniel dos Santos and Cainã Figueiredo Pereira
@email: leoleal@cos.ufrj.br, ddsantos@cos.ufrj.br, cainafpereira@cos.ufrj.br
@date: 2022-08-25
"""

import time
import copy

from utils.instancesRepresentation import OptimizationInstance

def solve(input: OptimizationInstance, **kwargs):
    problemInstance = input['problemInstance']
    solution = copy.deepcopy(problemInstance.solution)

    numberOfItems = problemInstance.numberOfItems
    numberOfKnapsacks = problemInstance.numberOfKnapsacks

    startTime = time.time() 
    foundTime =time.time()

    while 1:   
        bestSolutionFOValue = problemInstance.objective(solution, isMinimizing = False)

        bestItem = -1
        bestKnapsack = -1
        
        for i in range(numberOfItems):
            currentKnapsack = solution[i]
            for j in range(numberOfKnapsacks):
                solution[i] = j
                currentFOValue = problemInstance.objective(solution, isMinimizing = False)
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
    
    problemInstance.updateSolution(solution)

    timeToFindSolution = foundTime - startTime

    returnValue = {
        'problemInstance': problemInstance,
        'timeToFindSolution': timeToFindSolution
    }

    return returnValue