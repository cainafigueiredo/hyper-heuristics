# -*- coding: utf-8 -*-

"""
@author: Leonardo Rosas Leal, Daniel dos Santos and Cainã Figueiredo Pereira
@email: leoleal@cos.ufrj.br, ddsantos@cos.ufrj.br, cainafpereira@cos.ufrj.br
@date: 2022-08-25
"""

from typing import Callable, Dict, Text

from utils.pipelines import SequentialPipeline, Stage
from utils.instancesRepresentation import OptimizationInstance

from src.heuristics.constructive import randomConstructive
from src.heuristics.constructive import greedyConstruction
from src.heuristics.constructive import greedyRandomizedConstruction
from src.heuristics.localSearch import bestImprovement
from src.heuristics.localSearch import firstImprovement

from src.metaHeuristics import alns
from src.metaHeuristics import grasp
from src.metaHeuristics import geneticAlgorithm
from src.metaHeuristics import simulatedAnnealing
from src.metaHeuristics import tabuSearch

__seachSpace__ = {
    "randomConstructive": randomConstructive.solve,
    "greedyConstruction": greedyConstruction.solve,
    "greedyRandomizedConstruction": greedyRandomizedConstruction.solve,
    "bestImprovement": bestImprovement.solve,
    "firstImprovement": firstImprovement.solve,
    "alns": alns.solve,
    "grasp": grasp.solve,
    "simulatedAnnealing": simulatedAnnealing.solve,
    "tabuSearch": tabuSearch.solve,
    "geneticAlgorithm": geneticAlgorithm.solve
}

class HyperHeuristic():
    def __init__(self):
        self.pipeline = SequentialPipeline()

    def addHyperHeuristicComponent(self, component: Stage):
        return self.pipeline.addStage(component)

    def addHyperHeuristicComponentsFromDict(self, componentsDict: Dict):
        self.pipeline.loadStagesFromDict(componentsDict)
    
    def addHyperHeuristicComponentsFromJSON(self, componentsJSONPath: Text):
        self.pipeline.loadStagesFromJSON(componentsJSONPath)

    def getSolution(self, problemInstance: OptimizationInstance, callbackStage: Callable = None):
        input = {
            'problemInstance': problemInstance
        }
        return self.pipeline.process(input, callbackStage)

    def getStagesNames(self):
        return self.pipeline.getStagesNames()

    def getAvailableLowLevelHeuristics(self):
        return __seachSpace__

    def __str__(self):
        return self.pipeline.__str__()