# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 14:37:33 2022

@author: Leonardo
"""

import sys
sys.path.append('..')

from typing import Dict

def firstImprovementHeuristic(input: Dict, **params):
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
            
            - 'objectiveFunction': A function that calculates the objective function value given a solution.

            - 'solution': A solution for the problem instance.
    
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
    solution = [*input['solution']]

    numberOfItems = problemInstance['numberOfItems']
    numberOfKnapsacks = problemInstance['numberOfKnapsacks']

    while 1:
        #obtem a FO da solucao atual
        bestObjectiveFuntionValue = objectiveFunction(problemInstance, solution)
        #inicializa a variavel de controle da interrupcao da busca
        improved = False
        
        for i in range(numberOfItems):
            currentKnapsack = solution[i] #guarda a mochila atual
            for j in range(numberOfKnapsacks):
                solution[i] = j #altera a mochila e calcula a FO com a nova
                solution
                currentObjectiveFunctionValue = objectiveFunction(problemInstance, solution)
                if currentObjectiveFunctionValue > bestObjectiveFuntionValue: #se melhorar entao guarda as informacoes
                    improved = True #registra q melhorou
                    bestObjectiveFuntionValue = currentObjectiveFunctionValue #guarda a melhor FO
                    break #sai do laco de mochilas
            
            if improved:
                break #sai do laco de objetos
            else:
                solution[i] = currentKnapsack #restaura a mochila atual
        
        if not improved: #se nao melhorou interrompe
            break
    
    returnValue = {
        'problemInstance': problemInstance,
        'solution': solution,
        'foValue': objectiveFunction(problemInstance, solution)
    }

    return returnValue