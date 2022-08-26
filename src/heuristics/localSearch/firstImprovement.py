# -*- coding: utf-8 -*-

"""
@author: Leonardo Rosas Leal, Daniel dos Santos and Cainã Figueiredo Pereira
@email: leoleal@cos.ufrj.br, ddsantos@cos.ufrj.br, cainafpereira@cos.ufrj.br
@date: 2022-08-25
"""

import copy
from typing import Dict
from utils.instancesRepresentation import OptimizationInstance

def solve(input: OptimizationInstance, **kwargs):
    problemInstance = input['problemInstance']
    solution = copy.deepcopy(problemInstance.solution)

    numberOfItems = problemInstance.numberOfItems
    numberOfKnapsacks = problemInstance.numberOfKnapsacks

    while 1:
        bestSolutionFOValue = problemInstance.objective(solution, isMinimizing = False)
        improved = False
        
        for i in range(numberOfItems):
            currentKnapsack = solution[i]
            for j in range(1, numberOfKnapsacks + 1):
                solution[i] = j
                currentSolutionFOValue = problemInstance.objective(solution, isMinimizing = False)
                if currentSolutionFOValue > bestSolutionFOValue:
                    improved = True
                    bestSolutionFOValue = currentSolutionFOValue
                    break
            
            if improved:
                break
            else:
                solution[i] = currentKnapsack 
        
        if not improved:
            break
    
    problemInstance.updateSolution(solution)

    returnValue = {
        'problemInstance': problemInstance
    }

    return returnValue