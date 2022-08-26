# -*- coding: utf-8 -*-

"""
@author: Leonardo Rosas Leal, Daniel dos Santos and Cainã Figueiredo Pereira
@email: leoleal@cos.ufrj.br, ddsantos@cos.ufrj.br, cainafpereira@cos.ufrj.br
@date: 2022-08-25
"""

import time

from utils.instancesRepresentation import OptimizationInstance
from src.heuristics.localSearch import firstImprovement
from src.heuristics.constructive import greedyRandomizedConstruction

def __assertValidParams__(
    lrc: float,
    randomState: int,
    maxRunningTime: int, 
    noImprovementMaxIterations: int,
):
    assert lrc > 0 and lrc <= 1
    assert randomState >= 0
    assert maxRunningTime > 0
    assert noImprovementMaxIterations > 0

def solve(
        input: OptimizationInstance, 
        lrc: float = None,
        randomState: int = None,
        maxRunningTime: int = None, 
        noImprovementMaxIterations: int = None,
        **kwargs
    ):

    __assertValidParams__(
        lrc,
        randomState,
        maxRunningTime,
        noImprovementMaxIterations
    )

    problemInstance = input['problemInstance']

    startTime = time.time()
    foundTime = time.time()
    noImprovementIterationsCount = 0

    bestSolutionFOValue = float("-inf")
    
    while 1:
        currentSolution = greedyRandomizedConstruction.solve(input, lrc = lrc, randomState = randomState)['problemInstance']
        currentSolution = currentSolution.solution

        currentSolution = firstImprovement.solve(input)['problemInstance'].solution
        objectiveFunctionValue = input['problemInstance'].objective(currentSolution)
        
        if objectiveFunctionValue > bestSolutionFOValue:
            bestSolution = currentSolution
            bestSolutionFOValue = objectiveFunctionValue
            foundTime = time.time()
            noImprovementIterationsCount = 0
        else:
            noImprovementIterationsCount += 1
            if noImprovementIterationsCount >= noImprovementMaxIterations:
                break

        endTime = time.time()
        if endTime <= (startTime + maxRunningTime):
            continue
        else:
            break

    timeToFindSolution = foundTime - startTime

    returnValue = {
        'problemInstance': problemInstance,
        'timeToFindSolution': timeToFindSolution
    }

    return returnValue