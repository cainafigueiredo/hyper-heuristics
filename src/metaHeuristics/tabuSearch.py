# -*- coding: utf-8 -*-

"""
@author: Leonardo Rosas Leal, Daniel dos Santos and Cainã Figueiredo Pereira
@email: leoleal@cos.ufrj.br, ddsantos@cos.ufrj.br, cainafpereira@cos.ufrj.br
@date: 2022-08-25
"""

import time
import copy
import numpy as np

from utils.instancesRepresentation import OptimizationInstance

from typing import Dict

def __assertValidParams__(
    tabuListLen,
    maxSearchTimeInSeconds,
    noImprovementMaxIterations
):
    assert tabuListLen > 0
    assert maxSearchTimeInSeconds > 0
    assert noImprovementMaxIterations > 0

def solve(
        input: Dict, 
        tabuListLen: int = -1, 
        maxSearchTimeInSeconds: int = -1, 
        noImprovementMaxIterations: int = -1, 
        **kwargs
    ):

    __assertValidParams__(tabuListLen, maxSearchTimeInSeconds, noImprovementMaxIterations)

    problemInstance = input['problemInstance']
    initialSolution = copy.deepcopy(problemInstance).solution

    numberOfItems = problemInstance.numberOfItems
    numberOfKnapsacks = problemInstance.numberOfKnapsacks

    startTime = time.time()
    foundTime = time.time()
    noImprovementIterationsCount = 0

    nextFreePosTabuList = 0
    tabuList = np.zeros([2, tabuListLen])
    globalBestSolution = initialSolution
    globalBestSolutionFOValue = problemInstance.objective(globalBestSolution, isMinimizing = False)
    currentSolution = copy.copy(globalBestSolution)

    while 1:
        localBestSolutionFOValue = float("-inf") 
        
        bestItem = -1
        bestKnapsack = -1
        for i in range(numberOfItems):
            currentKnapsack = currentSolution[i]
            for j in range(numberOfKnapsacks+1):
                tabuListPositionPointer = -1
                aspirated = 0
                for k in range(tabuListLen):
                    if tabuList[0, k] == i and tabuList[1, k] == j:
                        tabuListPositionPointer= k
                        break
                
                currentSolution[i] = j
                currentSolutionFOValue = problemInstance.objective(currentSolution, isMinimizing = False)

                if tabuListPositionPointer == -1:
                    if currentSolutionFOValue > localBestSolutionFOValue:
                        bestItem = i
                        bestKnapsack = j
                        localBestSolutionFOValue = currentSolutionFOValue
                else:
                    if currentSolutionFOValue > globalBestSolutionFOValue:
                        bestItem = i
                        bestKnapsack = j
                        localBestSolutionFOValue = currentSolutionFOValue
                        aspirated = 1
                currentSolution[i] = currentKnapsack
        
        if bestItem != -1:
            currentSolution[bestItem] = bestKnapsack
            currentSolutionFOValue = localBestSolutionFOValue
            if (aspirated == 0):
                tabuList[0, nextFreePosTabuList] = bestItem
                tabuList[1, nextFreePosTabuList] = bestKnapsack
                nextFreePosTabuList += 1
                if nextFreePosTabuList >= tabuListLen:
                    nextFreePosTabuList = 0
        else:
            currentSolution[tabuList[0,0]] = tabuList[1,0]
            currentSolutionFOValue = localBestSolutionFOValue
        
        if currentSolutionFOValue > globalBestSolutionFOValue:
            foundTime = time.time()
            globalBestSolution = copy.copy(currentSolution)
            globalBestSolutionFOValue = currentSolutionFOValue
            noImprovementIterationsCount = 0
        else: 
            noImprovementIterationsCount += 1
            if noImprovementIterationsCount >= noImprovementMaxIterations:
                break
        
        endTime = time.time()
        if endTime <= (startTime + maxSearchTimeInSeconds):
            continue
        else:
            break
    
    problemInstance.updateSolution(globalBestSolution)

    timeToFindSolution = foundTime - startTime

    returnValue = {
        'problemInstance': problemInstance,
        'timeToFindSolution': timeToFindSolution
    }

    return returnValue
