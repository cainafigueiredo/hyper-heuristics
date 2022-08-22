# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 11:14:50 2022

@author: Leonardo
"""

import random as rand
from typing import Dict

def randomConstructiveHeuristic(input: Dict, **params):
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

    Results
    =======
        return: dict
            A dict with the following keys: 'problemInstance' (the same as the input), 'objectiveFunction' (FO calculation) and 'solution' (a random solution).
    """
    problemInstance = input['problemInstance']
    objectiveFunction = problemInstance['objectiveFunction']

    randomState = params.get("randomState", 0)
    rand.seed(randomState)

    numberOfItems = problemInstance['numberOfItems']
    numberOfKnapsacks = problemInstance['numberOfKnapsacks']

    solution = [0] * numberOfItems
        
    for item in range(numberOfItems):
        solution[item] = rand.randint(0, numberOfKnapsacks)
    
    returnValue = {
        'problemInstance': problemInstance,
        'solution': solution,
        'foValue': objectiveFunction(problemInstance, solution)
    }

    return returnValue