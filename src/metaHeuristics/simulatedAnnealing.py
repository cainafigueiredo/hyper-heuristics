# -*- coding: utf-8 -*-

"""
@author: Leonardo Rosas Leal, Daniel dos Santos and Cainã Figueiredo Pereira
@email: leoleal@cos.ufrj.br, ddsantos@cos.ufrj.br, cainafpereira@cos.ufrj.br
@date: 2022-08-25
"""

import time
import math as mat
import copy
import random as rand

from utils.instancesRepresentation import OptimizationInstance

def __assertValidParams__(
    saMax,
    coolingRate,
    startTemperature,
    freezingTemperature,
    randomState 
):
    assert saMax > 0
    assert coolingRate > 0 and coolingRate < 1
    assert startTemperature != None
    assert freezingTemperature != None
    assert randomState >= 0

def solve(
        input: OptimizationInstance,
        saMax: int = -1,
        coolingRate: float = -1,
        startTemperature: int = None,
        freezingTemperature: int = None,
        randomState: int = -1, 
        **kwargs
    ):

    __assertValidParams__(
        saMax,
        coolingRate,
        startTemperature,
        freezingTemperature,
        randomState
    )

    problemInstance = input['problemInstance']
    solution = copy.deepcopy(problemInstance.solution)

    numberOfItems = problemInstance.numberOfItems
    numberOfKnapsacks = problemInstance.numberOfKnapsacks

    rand.seed(randomState)

    startTime = time.time()
    foundTime = time.time()
    
    bestSolution = solution
    bestSolutionFOValue = problemInstance.objective(bestSolution, isMinimizing = False)
    
    currentSolution = copy.copy(bestSolution)
    currentSolutionFOValue = problemInstance.objective(currentSolution, isMinimizing = False)
    
    temperature = startTemperature
    while temperature > freezingTemperature:
        
        for i in range(saMax):
            neighborSolution = copy.copy(currentSolution)
            neighborSolution[rand.randint(0, numberOfItems-1)] = rand.randint(0, numberOfKnapsacks)
            neighborSolutionFOValue = problemInstance.objective(neighborSolution, isMinimizing = False)
            delta = currentSolutionFOValue - neighborSolutionFOValue
            
            if delta < 0:
                currentSolution = copy.copy(neighborSolution)
                if neighborSolutionFOValue > bestSolutionFOValue:
                    bestSolution = copy.copy(neighborSolution)
                    bestSolutionFOValue = neighborSolutionFOValue
                    foundTime = time.time()
            else:
                if rand.random() < mat.exp(-delta/temperature):
                    currentSolution = copy.copy(neighborSolution)
        
        temperature *= coolingRate
    
    timeToFindSolution = foundTime - startTime

    problemInstance.updateSolution(bestSolution)

    returnValue = {
        'problemInstance': problemInstance,
        'timeToFindSolution': timeToFindSolution
    }

    return returnValue