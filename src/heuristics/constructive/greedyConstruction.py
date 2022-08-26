# -*- coding: utf-8 -*-

"""
@author: Leonardo Rosas Leal, Daniel dos Santos and Cainã Figueiredo Pereira
@email: leoleal@cos.ufrj.br, ddsantos@cos.ufrj.br, cainafpereira@cos.ufrj.br
@date: 2022-08-25
"""

import numpy as np

from typing import Callable

from utils.instancesRepresentation import OptimizationInstance

def __assertValidParams__(sortIndexesFunction: Callable):
    assert sortIndexesFunction != None

def solve(
        input: OptimizationInstance, 
        sortIndexesFunction: Callable = None, 
        **kwargs
    ): 
    __assertValidParams__(sortIndexesFunction)

    problemInstance = input['problemInstance']

    numberOfItems = problemInstance.numberOfItems
    numberOfKnapsacks = problemInstance.numberOfKnapsacks
    itemsWeights = problemInstance.itemsWeights
    knapsacksCapacities = problemInstance.knapsacksCapacities

    solution = np.zeros(numberOfItems, dtype = int)
    totalKnapsacksCapacities = np.zeros(numberOfKnapsacks, dtype = int)
    
    orderedIndexes = sortIndexesFunction(problemInstance)
    
    for i in range(numberOfItems):
        for j in range(numberOfKnapsacks):
            if (totalKnapsacksCapacities[j] + itemsWeights[orderedIndexes[i]]) <= knapsacksCapacities[j]:
                solution[orderedIndexes[i]] = j + 1
                totalKnapsacksCapacities[j] += itemsWeights[orderedIndexes[i]]
                break

    problemInstance.updateSolution(solution)

    returnValue = {
        'problemInstance': problemInstance,
    }

    return returnValue