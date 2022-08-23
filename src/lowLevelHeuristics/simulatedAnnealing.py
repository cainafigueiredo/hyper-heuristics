# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 15:55:30 2022

@author: Leonardo
"""

import time
import math as mat
import copy as cpy
import random as rand

def simulatedAnnealingMetaHeuristic(input, **params):
    problemInstance = input['problemInstance']
    objectiveFunction = problemInstance['objectiveFunction']
    solution = input['solution']

    numberOfItems = problemInstance['numberOfItems']
    numberOfKnapsacks = problemInstance['numberOfKnapsacks']

    saMax = params['saMax']
    coolingRate = params['coolingRate']
    startTemperature = params['startTemperature']
    freezingTemperature = params['freezingTemperature']
    randomState = params.get('randomState', 0)

    rand.seed(randomState)

    startTime = time.time()
    foundTime = time.time()
    #guarda a solucao inicial como a melhor
    bestSolution = solution
    bestSolutionFOValue = objectiveFunction(problemInstance, bestSolution)
    #atribui a melhor solucao a sol atual
    currentSolution = cpy.copy(bestSolution)
    currentSolutionFOValue = objectiveFunction(problemInstance, currentSolution)
    #inicializa a temperatura
    temperature = startTemperature
    while temperature > freezingTemperature:
        #enquanto a temperatura inicial e maior que a temp de congelamento
        for i in range(saMax):
            #solucao vizinha inicia a partir da solucao atual
            neighborSolution = cpy.copy(currentSolution)
            #sorteia uma solucao vizinha
            neighborSolution[rand.randint(0, numberOfItems-1)] = rand.randint(0, numberOfKnapsacks)
            #calcula a FO da solucao vizinha
            neighborSolutionFOValue = objectiveFunction(problemInstance, neighborSolution)
            #calculando a variacao
            delta = currentSolutionFOValue - neighborSolutionFOValue
            
            if delta < 0:
                #se a variacao e negativa entao aceita
                currentSolution = cpy.copy(neighborSolution)
                if neighborSolutionFOValue > bestSolutionFOValue:
                    #se a FO da vizinha e melhor que a FO da FO global aceita
                    bestSolution = cpy.copy(neighborSolution)
                    bestSolutionFOValue = neighborSolutionFOValue
                    foundTime = time.time()
            else:
                if rand.random() < mat.exp(-delta/temperature):
                    #se nao e melhor mas aceita piorar
                    currentSolution = cpy.copy(neighborSolution)
        
        #resfria a temperatura
        temperature *= coolingRate
    
    timeToFindSolution = foundTime - startTime

    returnValue = {
        'problemInstance': problemInstance,
        'solution': bestSolution,
        'foValue': bestSolutionFOValue,
        'timeToFindSolution': timeToFindSolution
    }

    return returnValue