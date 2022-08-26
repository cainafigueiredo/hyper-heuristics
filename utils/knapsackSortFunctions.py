from typing import Dict
import numpy as np

def sortIndexesMostProfitable(problemInstance: Dict):
    orderedIndexes = np.array(problemInstance.itemsProfits)
    orderedIndexes = np.argsort(orderedIndexes)[::-1]
    return orderedIndexes

def sortIndexesByProfitWeightDensity(problemInstance: Dict):
    itemsProfits = np.array(problemInstance.itemsProfits)
    itemsWeights = np.array(problemInstance.itemsWeights)
    orderedIndexes = itemsProfits/itemsWeights # Element-wise division
    orderedIndexes = np.argsort(orderedIndexes)[::-1]
    return orderedIndexes