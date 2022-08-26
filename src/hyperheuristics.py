# -*- coding: utf-8 -*-

"""
@author: Leonardo Rosas Leal, Daniel dos Santos and Cainã Figueiredo Pereira
@email: leoleal@cos.ufrj.br, ddsantos@cos.ufrj.br, cainafpereira@cos.ufrj.br
@date: 2022-08-25
"""

from typing import Callable, Dict, Text
from utils.pipelines import SequentialPipeline, Stage
from utils.instancesRepresentation import OptimizationInstance

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

    def __str__(self):
        return self.pipeline.__str__()