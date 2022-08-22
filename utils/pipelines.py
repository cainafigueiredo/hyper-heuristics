from typing import Callable, Dict, List, Text

import json

class Stage():
    def __init__(self, name: Text, callback: Callable, inputSchema: List, outputSchema: List, params: Dict):
        self.name = name
        self.callback = callback
        self.inputSchema = set(inputSchema)
        self.outputSchema = set(outputSchema)
        self.params = params
        self.input = None
        self.output = None

    def isCompatibleWith(self, stage) -> bool:
        # Checking if the previous stage's output has all data required by the next stage's input
        return len(stage.inputSchema - self.outputSchema) == 0 # If 0, they are compatible

    def changeStageParams(self, newParams: Dict):
        self.params = newParams

    def getStageParams(self):
        return self.params

    def process(self, input) -> Dict:
        self.input = input
        output = self.callback(input, **self.params)
        self.output = output
        return output

    def __str__(self):
        text = "\n"
        text += f"Name: {self.name}\n"
        text += f"Params: {self.params}\n"
        text += f"Input: {self.input}\n"
        text += f"Output: {self.output}\n"

        return text

class SequentialPipeline():
    def __init__(self):
        self.stages = []

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

    def process(self, input: Dict):
        if self.hasStages():
            nextStageInput = input
            for stage in self.stages:
                currentStageOutput = stage.process(nextStageInput)
                nextStageInput = currentStageOutput
            return currentStageOutput
        else: 
            return None

    def __str__(self):
        text = ""
        if self.hasStages():
            for stage in self.stages:
                text += stage.__str__()
        else:
            text = "There are no stages in the pipeline."
        return text