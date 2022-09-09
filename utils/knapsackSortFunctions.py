from typing import Dict
import numpy as np

from src.KnapsackInstance import KnapsackInstance

def sortIndexesMostProfitable(problemInstance: KnapsackInstance):
    orderedIndexes = np.array(problemInstance.itemsProfits)
    orderedIndexes = np.argsort(orderedIndexes)[::-1]
    return orderedIndexes

def sortIndexesByProfitWeightDensity(problemInstance: KnapsackInstance):
    itemsProfits = np.array(problemInstance.itemsProfits)
    itemsWeights = np.array(problemInstance.itemsWeights)
    orderedIndexes = itemsProfits/itemsWeights # Element-wise division
    orderedIndexes = np.argsort(orderedIndexes)[::-1]
    return orderedIndexes



__availableSortIndexesFunctions = {
    'profit': sortIndexesMostProfitable,
    'density': sortIndexesByProfitWeightDensity
}

def getAvailableSortIndexesFunctions():
    return __availableSortIndexesFunctions