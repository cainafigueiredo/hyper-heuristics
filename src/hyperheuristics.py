import sys
sys.path.append('..')

from typing import List, Dict, Text
from utils.pipelines import SequentialPipeline, Stage
import lowLevelHeuristics

class HyperHeuristic():
    def __init__(self):
        self.pipeline = SequentialPipeline()

    def addHyperHeuristicComponent(self, component: Stage):
        return self.pipeline.addStage(component)

    def addHyperHeuristicComponentsFromDict(self, componentsDict: Dict):
        self.pipeline.loadStagesFromDict(componentsDict)
    
    def addHyperHeuristicComponentsFromJSON(self, componentsJSONPath: Text):
        self.pipeline.loadStagesFromJSON(componentsJSONPath)

    def printAvailableLowLevelHeuristics(self) -> List[Text]:
        lowLevelHeuristics.printAvailableLowLevelHeuristics()

    def getSolution(self, problemInstance):
        input = {
            'problemInstance': problemInstance
        }
        return self.pipeline.process(input)

    def __str__(self):
        return self.pipeline.__str__()