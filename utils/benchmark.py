import pandas as pd
import numpy as np
import copy
import os

from src.KnapsackInstance import KnapsackInstance

from typing import List, Text

class Benchmark:
    def __init__(self, name: Text, benchmarkRootPath: Text):
        self.name = name
        self.benchmarkRootPath = benchmarkRootPath

    def getInstancesList(self):
        raise NotImplemented

    def getOptimalFO(self, instance: Text):
        raise NotImplemented

    def parseInstance(self, instance: Text):
        raise NotImplemented

    def sampleInstance(self, n: int = 1):
        raise NotImplemented

class BinaryKnapsackBenchmark(Benchmark):
    def __init__(self, name: Text, benchmarkRootPath: Text):
        super().__init__(name, benchmarkRootPath)
        self._instancesList = self.getInstancesList()

    def getInstancesList(self) -> List[str]:
        instances = os.listdir(f"{self.benchmarkRootPath}/instances")
        instances = [f"{instance}/test.in" for instance in instances]
        return instances

    def getOptimalFO(self, instance: Text) -> int:
        optimalFOs = pd.read_csv(f'{self.benchmarkRootPath}/optima.csv')
        instanceName, _ = instance.split('/')
        return optimalFOs[optimalFOs['name'] == instanceName]['optimum'].values[0]

    def getOptimalRunningTime(self, instance: Text) -> float:
        instanceName, _ = instance.split('/')
        with open(f"{self.benchmarkRootPath}/instances/{instanceName}/time.out") as f:
            return float(f.readline().strip())

    def parseInstance(self, instance: Text) -> KnapsackInstance:
        numberOfItems = None
        numberOfKnapsacks = 1
        itemsProfits = []
        itemsWeights = []
        knapsacksCapacities = []

        with open(f"{self.benchmarkRootPath}/instances/{instance}") as f:
            numberOfItems = int(f.readline().strip())
            nextLine = [int(i) for i in f.readline().strip().split()]
            while len(nextLine) == 3:
                index, profit, weight = nextLine
                itemsProfits.append(profit)
                itemsWeights.append(weight)
                nextLine = [int(i) for i in f.readline().strip().split()]
            knapsacksCapacities.append(nextLine[0])

        solution = np.zeros(numberOfItems, dtype = int)

        knapsack = KnapsackInstance(
            numberOfItems = numberOfItems,
            numberOfKnapsacks = numberOfKnapsacks,
            itemsProfits = np.array(itemsProfits, dtype = int),
            itemsWeights = np.array(itemsWeights, dtype = int),
            knapsacksCapacities = np.array(knapsacksCapacities, dtype = int),
            solution = solution
        )
        return knapsack

    @staticmethod
    def toFile(instance: KnapsackInstance, filepath: Text):
        with open(filepath, 'w') as f:
            f.write(f"{instance.numberOfItems} {instance.numberOfKnapsacks}\n")
            f.write(" ".join([str(v) for v in instance.itemsProfits]) + "\n")
            f.write(" ".join([str(v) for v in instance.itemsWeights]) + "\n")
            f.write(" ".join([str(v) for v in instance.knapsacksCapacities]))

    def sampleInstance(self):
        sortedInstance = np.random.choice(self._instancesList)
        instance = self.parseInstance(sortedInstance)
        return sortedInstance, instance

    def split(self, trainFraction = 0.3):
        instances = copy.deepCopy(self._instancesList)
        np.sort(instances)
        trainSize = int(trainFraction  *len(instances))
        return [instances[:trainSize], instances[trainSize:]]
