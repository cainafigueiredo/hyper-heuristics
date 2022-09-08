import time

from typing import Optional
from numpy.random import RandomState

from alns.State import State
from alns.stop.StoppingCriterion import StoppingCriterion


class MaxRuntimeOrNoImprovement(StoppingCriterion):

    def __init__(self, max_runtime: float, max_iterations: int):
        if max_runtime < 0:
            raise ValueError("max_runtime < 0 not understood.")

        if max_iterations < 0:
            raise ValueError("max_iterations < 0 not understood.")

        self._max_runtime = max_runtime
        self._start_runtime: Optional[float] = None

        if max_iterations < 0:
            raise ValueError("max_iterations < 0 not understood.")

        self._max_iterations = max_iterations
        self._target: Optional[float] = None
        self._counter = 0

    @property
    def max_runtime(self) -> float:
        return self._max_runtime

    @property
    def max_iterations(self) -> int:
        return self._max_iterations

    def __call__(self, rnd: RandomState, best: State, current: State) -> bool:
        if self._start_runtime is None:
            self._start_runtime = time.perf_counter()

        if self._target is None or best.objective() < self._target:
            self._target = best.objective()
            self._counter = 0
        else:
            self._counter += 1

        stopRuntime = time.perf_counter() - self._start_runtime > self.max_runtime

        stopNoImprovement = self._counter >= self.max_iterations

        return stopRuntime or stopNoImprovement