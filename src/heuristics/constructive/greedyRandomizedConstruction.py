# -*- coding: utf-8 -*-

"""
@author: Leonardo Rosas Leal, Daniel dos Santos and Cainã Figueiredo Pereira
@email: leoleal@cos.ufrj.br, ddsantos@cos.ufrj.br, cainafpereira@cos.ufrj.br
@date: 2022-08-25
"""

import numpy as np
import random as rand

from utils.instancesRepresentation import OptimizationInstance

def __assertValidParams__(
    lrc: float,
    randomState: int
):
    assert lrc > 0 and lrc <= 1
    assert randomState > 0

def solve(
        input: OptimizationInstance, 
        lrc: float = None,
        randomState: int = None, 
        **kwargs
    ):

    __assertValidParams__(
        lrc,
        randomState
    )

    problemInstance = input['problemInstance']

    rand.seed(randomState)

    numberOfItems = problemInstance.numberOfItems
    numberOfKnapsacks = problemInstance.numberOfKnapsacks
    itemsProfits = problemInstance.itemsProfits
    itemsWeights = problemInstance.itemsWeights
    knapsacksCapacities = problemInstance.knapsacksCapacities

    auxVector = np.zeros(numberOfItems, dtype = int)

    lrcNumberOfCandidates = int(numberOfItems * lrc)
    profitsVector = np.zeros(lrcNumberOfCandidates, dtype = int)
    lrcVector = np.zeros(lrcNumberOfCandidates, dtype = int)
    
    for i in range(lrcNumberOfCandidates):
        randItem = rand.randint(0, numberOfItems - 1)
        while auxVector[randItem] == 1: #impede o sorteio de um numero repetido
            randItem = rand.randint(0, numberOfItems-1)
        
        lrcVector[i] = randItem
        profitsVector[i] = itemsProfits[randItem]
        auxVector[randItem] = 1
    
    orderedIndexesLRC = np.argsort(profitsVector)[::-1]

    solution = np.zeros(numberOfItems, dtype = int)
    vetPes = np.zeros(numberOfKnapsacks, dtype = int)
    for i in range(lrcNumberOfCandidates):
        for j in range(numberOfKnapsacks):
            if (vetPes[j] + itemsWeights[lrcVector[orderedIndexesLRC[i]]]) <= knapsacksCapacities[j]:
                solution[lrcVector[orderedIndexesLRC[i]]] = j + 1
                vetPes[j] = vetPes[j] + itemsWeights[lrcVector[orderedIndexesLRC[i]]]
                break

    vAuxIndObj = np.argsort(itemsProfits)[::-1]
    for i in range(numberOfItems):
        if auxVector[vAuxIndObj[i]] == 0:
            for j in range(numberOfKnapsacks):
                if (vetPes[j] + itemsWeights[vAuxIndObj[i]]) <= knapsacksCapacities[j]:
                    solution[vAuxIndObj[i]] = j + 1
                    vetPes[j] = vetPes[j] + itemsWeights[vAuxIndObj[i]]
                    break

    problemInstance.updateSolution(solution)

    returnValue = {
        'problemInstance': problemInstance,
    }

    return returnValue