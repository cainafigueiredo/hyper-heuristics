from abc import ABC, abstractmethod
from random import Random
from typing import List

import numpy as np
from numpy.random import RandomState
from src.operators.Operator import DestroyOperator, RepairOperator
from src.operators.DestroyOperators import RandomRemove
from src.local_search.LocalSearch import LocalSearch
from src.initial_solution.ConstructiveHeuristic import ConstructiveHeuristic

class WeightScheme(ABC):
    def __init__(self, scores: List[float], refinements, acceptances):
        num_refinement = len(refinements)
        num_acceptance = len(acceptances)
        
        self._validate_arguments(scores, num_refinement, num_acceptance)

        self._scores = scores
        self._refinement = refinements
        self._acceptance = acceptances
        self._refinement_weights = np.ones(num_refinement, dtype=float)
        self._acceptance_weights = np.ones(num_acceptance, dtype=float)

    @property
    def refinement_weights(self) -> np.ndarray:
        return self._refinement_weights

    @property
    def acceptance_weights(self) -> np.ndarray:
        return self._acceptance_weights
        
    def select_refinement(
        self, rnd_state: RandomState
    ) -> int:
        def select(refinement_weights, refinement_indexes):
            probs = refinement_weights / np.sum(refinement_weights)
            return rnd_state.choice(refinement_indexes, p=probs)

        destroyOrLocalSearchOrConstructiveIndexes = [i for i, refinement in enumerate(self._refinement) if isinstance(refinement[1], DestroyOperator) or isinstance(refinement[1], LocalSearch) or isinstance(refinement[1], ConstructiveHeuristic)]
        destroyOrLocalSearchOrConstructiveWeights = [self.refinement_weights[i] for i in destroyOrLocalSearchOrConstructiveIndexes]
        refinement_sorted_indexes = [select(destroyOrLocalSearchOrConstructiveWeights, destroyOrLocalSearchOrConstructiveIndexes)]

        if isinstance(self._refinement[refinement_sorted_indexes[0]][1], DestroyOperator):
            repairIndexes = [i for i, refinement in enumerate(self._refinement) if isinstance(refinement[1], RepairOperator)]
            repairWeights = [self.refinement_weights[i] for i in repairIndexes]
            refinement_sorted_indexes.append(select(repairWeights, repairIndexes))

        return refinement_sorted_indexes

    def select_acceptance(
        self, rnd_state: RandomState
    ) -> int:
        def select(acceptance_weights):
            probs = acceptance_weights / np.sum(acceptance_weights)
            return rnd_state.choice(range(len(acceptance_weights)), p=probs)

        acceptance_idx = select(self.acceptance_weights)

        return acceptance_idx

    @abstractmethod
    def update_weights(self, refinement_indexes: int, acceptance_idx, s_idx: int):
        return NotImplemented

    @staticmethod
    def _validate_arguments(scores, num_refinement, num_acceptance):
        if any(score < 0 for score in scores):
            raise ValueError("Negative scores are not understood.")

        if len(scores) < 4:
            # More than four is OK because we only use the first four.
            raise ValueError(f"Expected four scores, found {len(scores)}")

        if num_refinement <= 0:
            raise ValueError("Missing refinement methods.")

        if num_acceptance <= 0:
            raise ValueError("Missing acceptane criterion.")
