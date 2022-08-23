# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 17:39:56 2022

@author: 
"""

import numpy as np
import random as rand

def greedyRandConstructionHeuristic(input, **params):
    """
    Parameters
    ==========
        input: dict
            A dictionary with the following keys:
            - 'problemInstance': A dictionary with all the information about the problem instance 
                Usage example: 
                {
                    'numberOfItems': 10,
                    'numberOfWeights': 3,
                    'itemsProfits': [5,1,2,5,6,5,6,7,10,16],
                    'itemsWeights': [6,1,7,74,14,8,3,5,2,1],
                    'knapsacksCapacities': [15,6,25],
                    'objectiveFunction': knapsackObjectiveFunction
                }
    
        **params: 
            randomState: int (default: 0)
                The random seed for the random choices.

            lrc: float (default: 0.3)
                Fraction of candidates that will be in the restricted candidates list.

    Results
    =======
        return: dict
            A dict with the following keys: 'problemInstance' (the same as the input), 'objectiveFunction' (FO calculation) and 'solution' (a random solution).
    """ 
    problemInstance = input['problemInstance']
    objectiveFunction = problemInstance['objectiveFunction']

    lrc = params.get('lrc', 0.3)
    randomState = params.get('randomState', 0)
    rand.seed(randomState)

    numberOfItems = problemInstance['numberOfItems']
    numberOfKnapsacks = problemInstance['numberOfKnapsacks']
    itemsProfits = problemInstance['itemsProfits']
    itemsWeights = problemInstance['itemsWeights']
    knapsacksCapacities = problemInstance['knapsacksCapacities']

    auxVector = [0] * int(numberOfItems)

    lrcNumberOfCandidates = int(numberOfItems * lrc)
    profitsVector = [0] * int(lrcNumberOfCandidates)
    lrcVector = [0] * int(lrcNumberOfCandidates)
    
    for i in range(lrcNumberOfCandidates):
        randItem = rand.randint(0, numberOfItems-1)
        while auxVector[randItem] == 1: #impede o sorteio de um numero repetido
            randItem = rand.randint(0, numberOfItems-1)
        
        lrcVector[i] = randItem
        profitsVector[i] = itemsProfits[randItem]
        auxVector[randItem] = 1
    
    #inserir os objetos da LRC na mochila de forma gulosa
    #obtendo os indices dos objetos ordenados (descendente)
    orderedIndexesLRC = np.argsort(profitsVector)[::-1]
    
    solution = [0] * numberOfItems
    vetPes = [0] * numberOfKnapsacks
    for i in range(lrcNumberOfCandidates):
        for j in range(numberOfKnapsacks):
            if (vetPes[j] + itemsWeights[lrcVector[orderedIndexesLRC[i]]]) <= knapsacksCapacities[j]:
                solution[lrcVector[orderedIndexesLRC[i]]] = j
                vetPes[j] = vetPes[j] + itemsWeights[lrcVector[orderedIndexesLRC[i]]]
                break
    
    #inserir os demais objetos na mochila de forma gulosa
    vAuxIndObj = np.argsort(itemsProfits)[::-1]
    for i in range(numberOfItems):
        if auxVector[vAuxIndObj[i]] == 0: #se verdadeiro, entao nao foi alocado ainda
            for j in range(numberOfKnapsacks):
                if (vetPes[j] + itemsWeights[vAuxIndObj[i]]) <= knapsacksCapacities[j]:
                    solution[vAuxIndObj[i]] = j
                    vetPes[j] = vetPes[j] + itemsWeights[vAuxIndObj[i]]
                    break
    
    returnValue = {
        'problemInstance': problemInstance,
        'solution': solution,
        'foValue': objectiveFunction(problemInstance, solution)
    }

    return returnValue