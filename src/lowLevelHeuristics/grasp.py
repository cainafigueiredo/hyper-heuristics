# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 17:16:12 2022

@author: cyx3
"""

import time

from typing import Dict

from . import greedyRandomizedConstruction
from . import firstImprovement

def graspMetaHeuristic(input: Dict, **params):
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
            maxRunningTime: float (default: 10)
                Stop criteria for the GRASP search, in seconds. 

            randomState: int (default: 0)
                The random seed for the random choices in greedy randomized construction phase.

            lrc: float (default: 0.3)
                Fraction of candidates that will be in the restricted candidates list in greedy randomized construction phase.

    Results
    =======
        return: dict
            A dict with the following keys: 'problemInstance' (the same as the input), 'objectiveFunction' (FO calculation) and 'solution' (a random solution).
    """ 
    lrc = params.get('lrc', 0.3)
    randomState = params.get('randomState', 0)
    maxRunningTime = params.get('maxRunningTime', 10)
    
    problemInstance = input['problemInstance']
    objectiveFunction = problemInstance['objectiveFunction']

    numberOfItems = problemInstance['numberOfItems']

    startTime = time.time()
    foundTime = time.time()
    bestObjectiveFunctionValue = float("-inf") #obtendo valor infinito negativo
    lrc = (lrc * numberOfItems) / 100 #calculando o % da LRC com base nos objetos
    bestSolution = [0] * numberOfItems
    
    while 1:
        currentSolution = greedyRandomizedConstruction.greedyRandConstructionHeuristic(input, lrc = lrc, randomState = randomState)['solution']
        
        #calculando a FO da solucao construtiva aleatória inicial obtida
        #FO = CF.calcFO(sol, numberOfItems, numberOfKnapsacks, itemsProfits, itemsWeights,knapsacksCapacities) # Inserido por Leonardo

        #print("\nUma solução contrutiva inicial aleatória gulosa é:\n",sol) # Inserido por Leonardo
        #print("\nA FO da solução contrutiva aleatória gulosa é:\n",FO) # Inserido por Leonardo
        
        #busca local
        localSearchInput = {
            'problemInstance': problemInstance, 
            'solution': currentSolution
        }
        currentSolution = firstImprovement.firstImprovementHeuristic(localSearchInput)['solution']
        objectiveFunctionValue = objectiveFunction(problemInstance, currentSolution)
        
        if objectiveFunctionValue > bestObjectiveFunctionValue:
            bestSolution = currentSolution
            bestObjectiveFunctionValue = objectiveFunctionValue
            foundTime = time.time()
        
        endTime = time.time()
        #verifica se deve continuar executando
        if endTime <= (startTime + maxRunningTime):
            continue
        else:
            break
    
    timeToFindSolution = foundTime - startTime

    returnValue = {
        'problemInstance': problemInstance,
        'solution': bestSolution,
        'foValue': objectiveFunction(problemInstance, bestSolution),
        'timeToFindSolution': timeToFindSolution
    }

    return returnValue
