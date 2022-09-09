import logging
import time
import copy

from typing import Callable, Dict, Text, Tuple
from numpy import random as rnd

from src.initial_solution.ConstructiveHeuristic import ConstructiveHeuristic
from src.accept import AcceptanceCriterion
from src.stop import StoppingCriterion
from src.Statistics import Statistics
from src.weights import WeightScheme
from src.Result import Result
from src.State import State
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
        self._on_best = None

    @property
    def refinement(self):
        return list(self._refinement.items())

    @property
    def refinementNames(self):
        return list(self._refinement.keys())

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
        weight_scheme: WeightScheme,
        stop: StoppingCriterion,
        constructive_heuristic_name: Text = None,
        **kwargs,
    ) -> Result:
        if len(self._refinement) == 0:
            return ValueError("Refinement set is null.")
    
        if len(self._acceptance) == 0:
            return ValueError("Acceptance criterion set is null.")

        stats = Statistics()
        stats.collect_runtime(time.perf_counter())

        if constructive_heuristic_name is None:
            constructive_idx = weight_scheme.select_constructive(self._rnd_state)
            constructive_heuristic_name, constructive_heuristic = self.refinement[constructive_idx]
        else:
            constructive_heuristic = self._refinement[constructive_heuristic_name]
        
        initial_solution = constructive_heuristic(instance, self._rnd_state)
        init_obj = initial_solution.objective(isMinimizing = False)
    
        stats.collect_objective(init_obj)

        curr = copy.deepcopy(initial_solution)
        best = copy.deepcopy(initial_solution)

        while not stop(self._rnd_state, best, curr):
            # The current selection method is based on Roulette Choice
            # We randomly choose a low-level heuristic with a probability that is
            # proportional to its weight.  
            stats.collect_refinement_weights(weight_scheme._refinement_weights, self.refinementNames)
            
            refinement_indexes = weight_scheme.select_refinement(
                self._rnd_state
            )
            for refinement_idx in refinement_indexes:
                refinement_name, refinement_method = self.refinement[refinement_idx]
                cand = refinement_method(curr, self._rnd_state, **kwargs)

            crit_idx = weight_scheme.select_acceptance(
                self._rnd_state
            )
            crit_name, crit_method = self.acceptance[crit_idx]

            best, curr, s_idx = self._eval_cand(
                best, curr, cand, **kwargs
            )

            weight_scheme.update_weights(refinement_indexes, crit_idx, s_idx)

            stats.collect_objective(curr.objective(isMinimizing = False))
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
        best: State,
        curr: State,
        cand: State,
        **kwargs,
    ) -> Tuple[State, State, int]:
        w_idx = _REJECT

        accept_votes = 0
        reject_votes = 0
        for crit_name, crit in self.acceptance: 
            if crit(self._rnd_state, best, curr, cand):
                accept_votes += 1
            else: 
                reject_votes += 1 

        if accept_votes >= reject_votes:  # accept candidate
            w_idx = _BETTER if cand.objective() < curr.objective() else _ACCEPT
            curr = copy.deepcopy(cand)

        if cand.objective() < best.objective():  # candidate is new best
            # print(f"New best with objective {cand.objective():.2f}.")
            best = copy.deepcopy(cand)
            
            if self._on_best:
                cand = copy.deepcopy(self._on_best(best, self._rnd_state, **kwargs))

            return best, cand, _BEST

        return best, curr, w_idx
