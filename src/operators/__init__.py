from . import destroyOperators
from . import repairOperators

__availableOperators__ = {
    'randomRemove': destroyOperators.getRandomRemoveOperator,
    'worstRemove': destroyOperators.getWorstRemoveOperator,
    'randomRepair': repairOperators.getRandomRepairOperator,
    'greedyRepair': repairOperators.getGreedyRepairOperator
}

def getAvailableOperators():
    return __availableOperators__