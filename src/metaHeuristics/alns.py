# -*- coding: utf-8 -*-

"""
@author: Leonardo Rosas Leal, Daniel dos Santos and Cainã Figueiredo Pereira
@email: leoleal@cos.ufrj.br, ddsantos@cos.ufrj.br, cainafpereira@cos.ufrj.br
@date: 2022-08-25
"""

import numpy as np

from typing import List

from utils.instancesRepresentation import OptimizationInstance

from alns import ALNS
from alns.weights import SegmentedWeights
from alns.accept import SimulatedAnnealing
from alns.stop import NoImprovement

def __assertValidParams__(
    input,
    coolingRate,
    startTemperature,
    freezingTemperature,
    destroyOperators,
    repairOperators,
    rewards,
    segmentDecay,
    segmentLength,
    randomState,
    noImprovementMaxIterations,
):
    assert input != None
    assert destroyOperators.size > 0
    assert repairOperators.size > 0
    assert randomState > 0
    assert coolingRate >= 0 and coolingRate <= 1
    assert startTemperature != None
    assert freezingTemperature != None
    assert rewards.size == 4
    assert segmentDecay >= 0 and segmentDecay <= 1 
    assert segmentLength > 0
    assert noImprovementMaxIterations > 0

def solve(
        input: OptimizationInstance, 
        coolingRate: float = None,
        startTemperature: int = None,
        freezingTemperature: int = None,
        destroyOperators: np.array = np.array([]),
        repairOperators: np.array = np.array([]),
        rewards: np.array = np.array([]),
        segmentDecay: float = None,
        segmentLength: int = None,
        randomState: int = None,
        noImprovementMaxIterations: int = None,
        **kwargs
    ):

    __assertValidParams__(
        input, coolingRate, startTemperature, freezingTemperature,
        destroyOperators, repairOperators, rewards, segmentDecay,
        segmentLength, randomState, noImprovementMaxIterations
    )

    problemInstance = input['problemInstance']
    initialSolution = problemInstance

    randomState = np.random.RandomState(randomState)

    acceptanceCriteria = SimulatedAnnealing(
        start_temperature = startTemperature,
        end_temperature = freezingTemperature,
        step = coolingRate,
        method = 'exponential'
    )

    weightsScheme = SegmentedWeights(
        scores = rewards,
        num_destroy = len(destroyOperators),
        num_repair = len(repairOperators),
        seg_decay = segmentDecay,
        seg_length = segmentLength
    )

    stopCondition = NoImprovement(max_iterations = noImprovementMaxIterations)

    alns = ALNS(randomState)

    for destroyOperator in destroyOperators:
        alns.add_destroy_operator(destroyOperator)

    for repairOperator in repairOperators:
        alns.add_repair_operator(repairOperator)

    # It modifies the solution property directly in the instance object
    bestSolution = alns.iterate(initialSolution, weightsScheme, acceptanceCriteria, stopCondition).best_state.solution
    
    problemInstance.updateSolution(bestSolution)

    returnValue = {
        'problemInstance': problemInstance,
    }

    return returnValue