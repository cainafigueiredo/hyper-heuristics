import logging
import time

from typing import Callable, Dict, Tuple
from numpy import random as rnd

from initial_solution.ConstructiveHeuristic import ConstructiveHeuristic
from accept import AcceptanceCriterion
from stop import StoppingCriterion
from Statistics import Statistics
from weights import WeightScheme
from Result import Result
from State import State
# from operators.Operator import DestroyOperator, RepairOperator

_BEST = 0
_BETTER = 1
_ACCEPT = 2
_REJECT = 3

_RefinementType = Callable[[State, rnd.RandomState], State]

logger = logging.getLogger(__name__)

class HyperHeuristic:

    def __init__(self, rnd_state: rnd.RandomState = rnd.RandomState()):
        self._rnd_state = rnd_state
        self._refinement = {}
        self._acceptance: Dict[str, AcceptanceCriterion] = {}

    @property
    def refinement(self):
        return list(self._refinement.items())

    @property
    def acceptance(self):
        return list(self._acceptance.items())

    # TODO: reparação só pode após destruição. Destruição requer uma reparação
    def add_refinement(
        self,
        refinement: _RefinementType,
        name: str = None,
    ):
        self._refinement[name if name else refinement.__name__] = refinement

    def add_acceptance(
        self,
        acceptance: AcceptanceCriterion,
        name: str = None,
    ):
        self._acceptance[name if name else acceptance.__name__] = acceptance

    # TODO: Forçar uma reparação após uma destruição 
    def iterate(
        self,
        instance: State,
        constructive_heuristic: ConstructiveHeuristic,
        weight_scheme: WeightScheme,
        stop: StoppingCriterion,
        **kwargs,
    ) -> Result:
        if len(self._refinement) == 0:
            return ValueError("Refinement set is null.")
    
        if len(self._acceptance) == 0:
            return ValueError("Acceptance criterion set is null.")

        stats = Statistics()
        stats.collect_runtime(time.perf_counter())

        initial_solution = constructive_heuristic(self._rnd_state, instance, **kwargs)
        init_obj = initial_solution.objective()
 
        stats.collect_objective(init_obj)

        curr = best = initial_solution

        while not stop(self._rnd_state, best, curr):
            refinement_indexes = weight_scheme.select_refinement(
                self._rnd_state
            )
            for refinement_idx in refinement_indexes:
                refinement_name, refinement_method = self.refinement[refinement_idx]

                cand = refinement_method.iterate(curr, self._rnd_state, **kwargs)

            crit_idx = weight_scheme.select_acceptance(
                self._rnd_state
            )
            crit_name, crit_method = self.acceptance[crit_idx]

            best, curr, s_idx = self._eval_cand(
                crit_method, best, curr, cand, **kwargs
            )

            weight_scheme.update_weights(refinement_indexes, crit_idx, s_idx)

            stats.collect_objective(curr.objective())
            stats.collect_runtime(time.perf_counter())

        logger.info(f"Finished iterating in {stats.total_runtime:.2f}s.")

        return Result(best, stats)

    def on_best(self, func: _RefinementType):
        """
        Sets a callback function to be called when ALNS finds a new global best
        solution state.

        Parameters
        ----------
        func
            A function that should take a solution State as its first argument,
            and a numpy RandomState as its second (cf. the operator signature).
            It should return a (new) solution State.
        """
        logger.debug(f"Adding on_best callback {func.__name__}.")
        self._on_best = func

    def _eval_cand(
        self,
        crit: AcceptanceCriterion,
        best: State,
        curr: State,
        cand: State,
        **kwargs,
    ) -> Tuple[State, State, int]:
        """
        Considers the candidate solution by comparing it against the best and
        current solutions. Candidate solutions are accepted based on the
        passed-in acceptance criterion. The (possibly new) best and current
        solutions are returned, along with a weight index (best, better,
        accepted, rejected).

        Returns
        -------
        A tuple of the best and current solution, along with the weight index.
        """
        w_idx = _REJECT

        if crit(self._rnd_state, best, curr, cand):  # accept candidate
            w_idx = _BETTER if cand.objective() < curr.objective() else _ACCEPT
            curr = cand

        if cand.objective() < best.objective():  # candidate is new best
            logger.info(f"New best with objective {cand.objective():.2f}.")

            # if self._on_best:
            #     cand = self._on_best(cand, self._rnd_state, **kwargs)

            return cand, cand, _BEST

        return best, curr, w_idx
