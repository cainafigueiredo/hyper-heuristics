# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 11:14:50 2022

@author: Leonardo
"""

from typing import Dict
import numpy as np

def sortIndexesMostProfitable(problemInstance: Dict):
    orderedIndexes = np.array(problemInstance['itemsProfits'])
    orderedIndexes = np.argsort(orderedIndexes)[::-1]
    return orderedIndexes

def greedyConstructionHeuristic(input: Dict, **params): 
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
            sortIndexesFunction: function (default: sort by items' profits)
                A function that receives the problem instance and return a list of the indexes (items) sorted according a given criteria. 

    Results
    =======
        return: dict
            A dict with the following keys: 'problemInstance' (the same as the input), 'objectiveFunction' (FO calculation) and 'solution' (a random solution).
    """
    problemInstance = input['problemInstance']
    objectiveFunction = problemInstance['objectiveFunction']

    sortIndexesFunction = params.get('sortIndexesFunction', sortIndexesMostProfitable)

    numberOfItems = problemInstance['numberOfItems']
    numberOfKnapsacks = problemInstance['numberOfKnapsacks']
    itemsWeights = problemInstance['itemsWeights']
    knapsacksCapacities = problemInstance['knapsacksCapacities']

    solution = [0] * numberOfItems
    #este vetor e utilizado para armazenar o peso alocado em cada mochila
    totalKnapsacksCapacities = [0] * numberOfKnapsacks
    
    #obtendo os indices dos objetos ordenados (descendente)
    orderedIndexes = sortIndexesFunction(problemInstance)
    
    for i in range(numberOfItems):
        #percorrendo os objetos
        for j in range(1, numberOfKnapsacks):
            #verifica se o objeto cabe na mochila
            if (totalKnapsacksCapacities[j-1] + itemsWeights[orderedIndexes[i]]) <= knapsacksCapacities[j-1]:
                solution[orderedIndexes[i]] = j
                totalKnapsacksCapacities[j-1] += itemsWeights[orderedIndexes[i]]
                break #se alocou o objeto na mochila, sai
    
    returnValue = {
        'problemInstance': problemInstance,
        'solution': solution,
        'foValue': objectiveFunction(problemInstance, solution)
    }

    return returnValue

