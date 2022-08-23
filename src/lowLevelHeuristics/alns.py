from copy import copy
import numpy as np

from dataclasses import dataclass
from typing import Dict, List

from alns import ALNS, State
from alns.weights import SegmentedWeights
from alns.accept import SimulatedAnnealing
from alns.stop import NoImprovement

@dataclass
class ProblemInstanceState(State):
    solution: List
    problemInstance: Dict

    def objective(self) -> float:
        objectiveFunction = self.problemInstance['objectiveFunction']
        return -objectiveFunction(self.problemInstance, self.solution) # ALNS expects a minimization problem


def randomRemove(state: ProblemInstanceState, randomState: int):
    pass

def worstRemove(state: ProblemInstanceState, randomState: int):
    pass

def randomRepair(state: ProblemInstanceState, randomState: int):
    pass

def greedyRepair(state: ProblemInstanceState, randomState: int):
    pass

def ALNSMetaHeuristic(input: Dict, **params):
    problemInstance = input['problemInstance']
    objectiveFunction = problemInstance['objectiveFunction']
    initialSolution = ProblemInstanceState(input['solution'], input['problemInstance'])

    destroyOperators = params['destroyOperators']
    repairOperators = params['repairOperators']
    randomState = params['randomState']
    randomState = np.random.RandomState(randomState)

    startTemperature = params['startTemperature']
    freezingTemperature = params['freezingTemperature']
    coolingRate = params['coolingRate']
    acceptanceCriteria = SimulatedAnnealing(
        start_temperature = startTemperature,
        end_temperature = freezingTemperature,
        step = coolingRate,
        method = 'exponential'
    )

    rewards = params['rewards']
    segmentDecay = params['segmentDecay']
    segmentLength = params['segmentLength']
    weightsScheme = SegmentedWeights(
        scores = rewards,
        num_destroy = len(destroyOperators),
        num_repair = len(repairOperators),
        seg_decay = segmentDecay,
        seg_length = segmentLength
    )

    noImprovementMaxIterations = params['noImprovementMaxIterations']
    stopCondition = NoImprovement(max_iterations = noImprovementMaxIterations)

    alns = ALNS(randomState)

    for destroyOperator in destroyOperators:
        alns.add_destroy_operator(destroyOperator)

    for repairOperator in repairOperators:
        alns.add_repair_operator(repairOperator)

    alns.iterate(initialSolution, weightsScheme, acceptanceCriteria, stopCondition)

    bestSolution = alns.best.solution
    bestSolutionFOValue = objectiveFunction(problemInstance, objectiveFunction)

    returnValue = {
        'problemInstance': problemInstance,
        'solution': bestSolution,
        'foValue': bestSolutionFOValue
    }