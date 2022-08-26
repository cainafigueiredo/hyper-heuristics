from typing import Callable, Dict, List, Text

import json
from time import time

class Stage():
    def __init__(self, name: Text, callback: Callable, inputSchema: List, outputSchema: List, params: Dict):
        self.name = name
        self.callback = callback
        self.inputSchema = set(inputSchema)
        self.outputSchema = set(outputSchema)
        self.params = params
        self.input = None
        self.output = None
        self.processTime = None

    def isCompatibleWith(self, stage) -> bool:
        # Checking if the previous stage's output has all data required by the next stage's input
        return len(stage.inputSchema - self.outputSchema) == 0 # If 0, they are compatible

    def changeStageParams(self, newParams: Dict):
        self.params = newParams

    def getStageParams(self):
        return self.params

    def process(self, input) -> Dict:
        self.input = input
        
        startTime = time()
        output = self.callback(input, **self.params)
        finalTime = time()
        
        self.output = output

        self.processTime = finalTime - startTime

        return output

    def __str__(self):
        text = "\n"
        text += f"- Name: {self.name}\n"
        text += f"- Params: {self.params}\n"
        text += f"- Input: {self.input}\n"
        text += f"- Output: {self.output}\n"
        text += f"- Running time: {self.processTime:.9f}s\n"

        return text

class SequentialPipeline():
    def __init__(self):
        self.stages = []
        self.processTime = None

    def hasStages(self) -> bool:
        return len(self.stages) != 0

    def getLastStage(self) -> Stage:
        if not self.hasStages():
            return None
        else:
            return self.stages[-1]

    def addStage(self, stage: Stage):
        if not self.hasStages() or (self.getLastStage().isCompatibleWith(stage)):
            self.stages += [stage]
            return stage
        else:
            return None

    def loadStagesFromDict(self, components: List[Dict]):
        # Getting stages objects from components information
        stages = []
        hasStages = False

        for stageInfo in components:
            name = stageInfo['name']
            callback = stageInfo['callback']
            inputSchema = stageInfo['inputSchema']
            outputSchema = stageInfo['outputSchema']
            params = stageInfo['params']
            stage = Stage(name, callback, inputSchema, outputSchema, params)
            if not hasStages:
                stages += [stage]
            else: 
                lastStage = stages[-1]
                if not lastStage.isCompatibleWith(stage):
                    return None
                else:
                    stages += [stage]
        
        # Adding stages to the pipeline
        for stage in stages:
            self.addStage(stage)

        return 0

    def loadStagesFromJSON(self, componentsJSONPath: Text):
        components = json.loads(componentsJSONPath)
        return self.loadStagesFromDict(components)

    def process(self, input: Dict, callbackStage: Callable = None):
        if self.hasStages():
            self.processTime = 0
            nextStageInput = input
            for stage in self.stages:
                currentStageOutput = stage.process(nextStageInput)
                self.processTime += stage.processTime
                
                if not callbackStage is None: 
                    callbackStage(stage)

                nextStageInput = currentStageOutput
            return currentStageOutput
        else: 
            return None

    def __str__(self):
        text = f"Total running time: {self.processTime:.9f}s\n"
        if self.hasStages():
            for stage in self.stages:
                text += stage.__str__()
        else:
            text = "There are no stages in the pipeline."
        return text