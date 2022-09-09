from collections import defaultdict
from typing import DefaultDict, List

import numpy as np


class Statistics:
    """
    Statistics object that stores some iteration results. Populated by the ALNS
    algorithm.
    """

    def __init__(self):
        self._objectives = []
        self._runtimes = []

        self._destroy_operator_counts = defaultdict(lambda: [0, 0, 0, 0])
        self._repair_operator_counts = defaultdict(lambda: [0, 0, 0, 0])
        self._refinement_weights = []

    @property
    def objectives(self) -> np.ndarray:
        """
        Returns an array of previous objective values, tracking progress.
        """
        return self._objectives

    @property
    def refinement_weights(self) -> np.ndarray:
        return self._refinement_weights

    @property
    def start_time(self) -> float:
        """
        Return the reference start time to compute the runtimes.
        """
        return self._runtimes[0]

    @property
    def total_runtime(self) -> float:
        """
        Return the total runtime (in seconds).
        """
        return self._runtimes[-1] - self._runtimes[0]

    @property
    def runtimes(self) -> np.ndarray:
        """
        Returns an array of iteration run times (in seconds).
        """
        return np.diff(self._runtimes)

    def collect_objective(self, objective: float):
        """
        Collects an objective value.

        Parameters
        ----------
        objective
            The objective value to be collected.
        """
        self._objectives.append(objective)

    def collect_runtime(self, time: float):
        """
        Collects the time one iteration took.

        Parameters
        ----------
        time
            Time in seconds.
        """
        self._runtimes.append(time)

    def collect_refinement_weights(self, refinements_weights, refinements_names):
        weights = {refinement_name: refinements_weights[i] for i, refinement_name in enumerate(refinements_names)}
        self._refinement_weights.append(weights)
