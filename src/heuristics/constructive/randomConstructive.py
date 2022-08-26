# -*- coding: utf-8 -*-

"""
@author: Leonardo Rosas Leal, Daniel dos Santos and Cainã Figueiredo Pereira
@email: leoleal@cos.ufrj.br, ddsantos@cos.ufrj.br, cainafpereira@cos.ufrj.br
@date: 2022-08-25
"""

import random as rand
import numpy as np

from utils.instancesRepresentation import OptimizationInstance

def solve(
        input: OptimizationInstance, 
        randomState: int = -1,    
        **kwargs
    ):
    assert randomState >= 0

    problemInstance = input['problemInstance']

    rand.seed(randomState)

    numberOfItems = problemInstance.numberOfItems
    numberOfKnapsacks = problemInstance.numberOfKnapsacks

    solution = np.zeros(numberOfItems, dtype = int)
        
    for item in range(numberOfItems):
        solution[item] = rand.randint(0, numberOfKnapsacks)

    problemInstance.updateSolution(solution)

    returnValue = {
        'problemInstance': problemInstance,
    }

    return returnValue