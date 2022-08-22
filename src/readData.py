# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 20:36:36 2022

@author: Leonardo

"""

from typing import Text
import numpy as np
from evaluation import objectiveFunction

def readData(datapath: Text, objectiveFunctionPenalty: float):
    #inicializando as variaveis
    numObj = numMoc = 0
    valObj = []
    pesObj = []
    capMoc = []
    #lendo os dados
    f = open(datapath)
    
    #lendo a primeira linha
    linha = f.readline()
    valores = linha.split()
    #lendo o numero de objetos
    numObj = int(valores[0])
    #lendo o numero de mochilas
    numMoc = int(valores[1])
    
    #Printando numObj e numMoc
    # print("O numObj e numMoc são:\n",numObj,numMoc)
    
    #lendo a segunda linha
    
    linha = f.readline()
    valores = linha.split()
    #lendo os valores dos objetos
    for val in valores:
        valObj.append(int(val))
        
    #Printando os valores
    # print("\nOs valores são:\n",valObj)
    
        
    
    #lendo a terceira linha
    linha = f.readline()
    valores = linha.split()
    #lendo os pesos dos objetos
    for val in valores:
        pesObj.append(int(val))
        
    #Printando os pesos dos objetos
    # print("\nOs pesos são:\n",pesObj)
    densValor=np.array(valObj)/np.array(pesObj)
    densValor=densValor.round(2)
    # print("\nA densidade de valor é:\n",densValor) # Leonardo
    
    
    #lendo a quarta linha
    linha = f.readline()
    valores = linha.split()
    #lendo a capacidade das mochilas
    for val in valores:
        capMoc.append(int(val))
    
    #Printando as capacidades das mochilas
    # print("\nAs capacidades são:\n",capMoc)
    
    f.close()

    def newObjectiveFunction(problemInstance, solution):
        return objectiveFunction(problemInstance, solution, noFeasiblePenalty = objectiveFunctionPenalty)

    returnValue = {
        'numberOfItems': numObj,
        'numberOfKnapsacks': numMoc,
        'itemsProfits': valObj,
        'itemsWeights': pesObj,
        'knapsacksCapacities': capMoc,
        'objectiveFunction': newObjectiveFunction
    }

    return returnValue