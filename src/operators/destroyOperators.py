import copy
from collections import Counter, defaultdict
from typing import List, Text
import numpy as np
from src import State

from utils.knapsackSortFunctions import sortIndexesByProfitWeightDensity
from .Operator import DestroyOperator

class RandomRemove(DestroyOperator):
    def __init__(self, destroyRate: float):
        self.destroyRate = destroyRate

    def __call__(self, instance: State, randomState: int = 0):
        copyInstance = copy.deepcopy(instance)

        numberOfItems = instance.numberOfItems

        numberOfItemToRemove = int(numberOfItems*self.destroyRate)
        itemsToRemove = randomState.choice(
            np.arange(numberOfItems), 
            replace = False,
            size = numberOfItemToRemove
        ) 

        for itemToRemove in itemsToRemove:
            copyInstance.solution[itemToRemove] = 0

        return copyInstance

class WorstRemove(DestroyOperator):
    def __init__(self, destroyRate: float, sortIndexesFunction = sortIndexesByProfitWeightDensity):
        self.destroyRate = destroyRate
        self.sortIndexesFunction = sortIndexesFunction

    def __call__(self, instance: State, randomState: int = 0):        
        copyInstance = copy.deepcopy(instance)

        numberOfItems = instance.numberOfItems

        numberOfItemsToRemove = int(numberOfItems*self.destroyRate)

        orderedIndexes = self.sortIndexesFunction(instance)[::-1]
        itemsToRemove = orderedIndexes[:numberOfItemsToRemove]

        for itemToRemove in itemsToRemove:
            copyInstance.solution[itemToRemove] = 0

        return copyInstance

class ShawRemove(DestroyOperator):
    def __init__(self, criteria: Text = 'profit'):
        self.criteria = criteria

    def __call__(self, instance: State, randomState: int = 0):        
        copyInstance = copy.deepcopy(instance)
        solution = copyInstance.solution

        if self.criteria == 'profit':
            crit = copyInstance.itemsProfits
        else: 
            raise NotImplemented

        def duplicates(lst):
            cnt= Counter(lst)
            return [key for key in cnt.keys() if cnt[key]> 1]
        
        def indices(lst, items= None):
            items, ind= set(lst) if items is None else items, defaultdict(list)
            for i, v in enumerate(lst):
                if v in items: ind[v].append(i)
            return ind

        Duplicates=duplicates(crit) 
        Indices=indices(crit)
                    
        for x in Duplicates:
            setElemToDest=Indices[x]
            while 1:
                indx=setElemToDest[randomState.randint(0,len(setElemToDest))]
                if solution[indx]!=0:
                    solution[indx]=0
                    break
                else:
                    continue
        
        copyInstance.solution = solution
        
        return copyInstance