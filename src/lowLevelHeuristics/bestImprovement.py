# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 14:37:33 2022

@author: Leonardo
"""

from typing import Dict
import time # Leonardo

def bestImprovementHeuristic(input: Dict, **params):
    problemInstance = input['problemInstance']
    objectiveFunction = problemInstance['objectiveFunction']
    solucao = input['solution']

    numberOfItems = problemInstance['numberOfItems']
    numberOfKnapsacks = problemInstance['numberOfKnapsacks']

    ini = time.time() # Marca o instante de início. Leonardo
    achouT =time.time() # Leonardo
    while 1:   
        #obtem a FO da solucao atual
        
        mFO = objectiveFunction(problemInstance, solucao)
        #inicializa as variaveis que vao armazenar
        #o controle de troca de objeto e mochila
        mO = -1
        mM = -1
        
        for i in range(numberOfItems):
            mAtual = solucao[i] #guarda a mochila atual
            for j in range(numberOfKnapsacks):
                solucao[i] = j #altera a mochila e calcula a FO da nova solucao
                FOAtual = objectiveFunction(problemInstance, solucao)
                if FOAtual > mFO: #se melhorar entao guarda as posicoes
                    mO = i
                    mM = j
                    mFO = FOAtual
                    
                
            solucao[i] = mAtual #restaura a mochila atual
        
        if mO!=-1: #se verdadeiro entao houve melhora
            solucao[mO] = mM #guarda a melhora que ocorreu
            achouT = time.time()# Leonardo
        else:
            break #se nao tem como mais melhorar, termina
    
    timeToFindSolution = achouT-ini

    returnValue = {
        'problemInstance': problemInstance,
        'solution': solucao,
        'foValue': mFO,
        'timeToFindSolution': timeToFindSolution
    }

    return returnValue,  # Leonardo, inserção de (achouT - ini)