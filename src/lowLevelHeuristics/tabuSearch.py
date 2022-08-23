import time
import copy as cpy
import numpy as np

from typing import Dict

def tabuSearchMetaHeuristic(input: Dict, **params):
    problemInstance = input['problemInstance']
    objectiveFunction = problemInstance['objectiveFunction']
    initialSolution = input['solution']

    numberOfItems = problemInstance['numberOfItems']
    numberOfKnapsacks = problemInstance['numberOfKnapsacks']

    tabuListLen = params['tabuListLen']
    maxSearchTime = params['maxSearchTime']

    startTime = time.time()
    foundTime = time.time()

    nextFreePosTabuList = 0
    tabuList = np.zeros([2, tabuListLen])
    bestSolution = initialSolution
    #calcula a FO da solucao
    globalBestSolutionFOValue = objectiveFunction(problemInstance, bestSolution)
    currentSolution = cpy.copy(bestSolution)
    while 1:
        #melhor vizinho
        localBestSolutionFOValue = float("-inf") #obtendo valor infinito negativo
        
        bestItem = -1
        bestKnapsack = -1
        for i in range(numberOfItems):
            currentKnapsack = currentSolution[i] #guarda a mochila atual do objeto
            for j in range(numberOfKnapsacks):
                #verificar a posicao da lista Tabu
                tabuListPositionPointer = -1
                aspirated = 0
                for k in range(tabuListLen):
                    if tabuList[0, k] == i and tabuList[1, k] == j:
                        tabuListPositionPointer= k
                        break
                
                currentSolution[i] = j
                currentSolutionFOValue = objectiveFunction(problemInstance, currentSolution)

                if tabuListPositionPointer== -1:
                    #a configuracao nao esta na lista tabu
                    if currentSolutionFOValue > localBestSolutionFOValue:
                        bestItem = i
                        bestKnapsack = j
                        localBestSolutionFOValue = currentSolutionFOValue
                else:
                    #esta na lista tabu, mas a FO e melhor que a FO Global
                    if currentSolutionFOValue > globalBestSolutionFOValue:
                        #aspiracao por objetivo
                        bestItem = i
                        bestKnapsack = j
                        localBestSolutionFOValue = currentSolutionFOValue
                        #salva um flag para nao incluir na lista tabu novamente
                        aspirated = 1
                #ajustando para mochila original
                currentSolution[i] = currentKnapsack
        
        #atualizando a lista Tabu
        if bestItem != -1:
            #algum vizinho foi aceito
            currentSolution[bestItem] = bestKnapsack #o objeto na posicao aceita recebe a melhor mochila
            currentSolutionFOValue = localBestSolutionFOValue #atualiza a FO
            if (aspirated == 0): #nao usou o criterio de aspiracao        
                tabuList[0, nextFreePosTabuList] = bestItem
                tabuList[1, nextFreePosTabuList] = bestKnapsack
                nextFreePosTabuList += 1
                if nextFreePosTabuList >= tabuListLen:
                    nextFreePosTabuList = 0
        else:
            #nenhum vizinho aceito
            currentSolution[tabuList[0,0]] = tabuList[1,0] #realiza a aspiracao por default
            currentSolutionFOValue = localBestSolutionFOValue #atualiza a FO
        
        if currentSolutionFOValue > globalBestSolutionFOValue:
            foundTime = time.time()
            bestSolution = cpy.copy(currentSolution)
            globalBestSolutionFOValue = currentSolutionFOValue
            print(globalBestSolutionFOValue)
        
        endTime = time.time()
        #verifica se deve continuar executando
        if endTime <= (startTime + maxSearchTime):
            continue
        else:
            globalBestSolutionFOValue
            break
    
    timeToFindSolution = foundTime - startTime

    returnValue = {
        'problemInstance': problemInstance,
        'solution': bestSolution,
        'foValue': globalBestSolutionFOValue,
        'timeToFindSolution': timeToFindSolution
    }

    return returnValue
