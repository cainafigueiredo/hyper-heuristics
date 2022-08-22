# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:15:54 2022

@author: Leonardo
"""

from typing import Dict

def objectiveFunction(problemInstance: Dict, solution, noFeasiblePenalty: float):
    numberOfItems = problemInstance['numberOfItems']
    numberOfKnapsacks = problemInstance['numberOfKnapsacks']
    itemsProfits = problemInstance['itemsProfits']
    itemsWeights = problemInstance['itemsWeights']
    knapsacksCapacities = problemInstance['knapsacksCapacities']

    foValue = 0
    totalKnapsacksWeights = [0] * numberOfKnapsacks
    
    for i in range(numberOfItems):
        #calcula a FO dos objetos selecionados
        if solution[i] != 0:
            foValue += itemsProfits[i]
            totalKnapsacksWeights[solution[i]-1] += itemsWeights[i]
    
    for j in range(numberOfKnapsacks):
        #verifica se a capacidade da mochila foi excedida
        if totalKnapsacksWeights[j] > knapsacksCapacities[j]:
            #se verdadeiro penaliza a FO
            foValue -= noFeasiblePenalty * (totalKnapsacksWeights[j] - knapsacksCapacities[j])
    
    return foValue