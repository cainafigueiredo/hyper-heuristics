import logging
import time
import copy

from typing import Callable, List, Text, Tuple
from numpy import random as rnd

from src.initial_solution.ConstructiveHeuristic import ConstructiveHeuristic
from src.accept import AcceptanceCriterion
from src.stop import StoppingCriterion
from src.State import State
# from operators.Operator import DestroyOperator, RepairOperator

_BEST = 0
_BETTER = 1
_ACCEPT = 2
_REJECT = 3

_RefinementType = Callable[[State, rnd.RandomState], State]

logger = logging.getLogger(__name__)

class HyperHeuristic:

    def __init__(
        self, 
        stop: StoppingCriterion = None, 
        acceptance: AcceptanceCriterion = None, 
        rewards: List = [1,1,1,1], 
        rnd_state: rnd.RandomState = rnd.RandomState(),
        on_best: Callable[[State], State] = lambda cand: cand
    ):
        self._rnd_state = rnd_state
        self._rewards = rewards
        self._refinement = {}
        self._acceptance = acceptance
        self._stop = stop
        self._on_best = None
        self._current_solution = None
        self._best_solution = None
        self._candidate_solution = None

    @property
    def current_solution(self):
        return self._current_solution
   
    @property
    def best_solution(self):
        return self._best_solution

    @property
    def refinement(self):
        return list(self._refinement.items())

    @property
    def refinementNames(self):
        return list(self._refinement.keys())

    @property
    def acceptance(self):
        return self._acceptance

    # TODO: reparação só pode após destruição. Destruição requer uma reparação
    def add_refinement(
        self,
        refinement: _RefinementType,
        name: str = None,
    ):
        self._refinement[name if name else refinement.__name__] = refinement

    def get_reward(self, rewardStatus):
        return self._rewards[rewardStatus]

    def initial_solution(self, instance, constructive_heuristic_name: Text = None, rnd_state = rnd.RandomState(0)):
        if constructive_heuristic_name is None:
            constructiveIDs = [heuristicName for heuristicName, heuristic in self.refinement if isinstance(heuristic, ConstructiveHeuristic)]
            constructive_heuristic_name = rnd_state.choice(constructiveIDs)
            constructive_heuristic = self._refinement[constructive_heuristic_name]
        else:
            constructive_heuristic = self._refinement[constructive_heuristic_name]
            
        initial_solution = constructive_heuristic(instance, self._rnd_state)
        
        self._current_solution = copy.deepcopy(initial_solution)
        self._best_solution = copy.deepcopy(initial_solution)

        return initial_solution

    def refine(self, current_solution, refinement_name: Text):
        assert refinement_name in self._refinement, "Low-Level Heuristic does not exist"
        refinement_method = self._refinement[refinement_name]
        candidate_solution = refinement_method(current_solution, self._rnd_state)

        self._candidate_solution = copy.deepcopy(candidate_solution)

        return candidate_solution

    def eval_stop(self, rnd_state: rnd.RandomState, best, curr):
        return self._stop(rnd_state, best, curr)

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

    def eval_cand(self) -> Tuple[State, State, int]:
        w_idx = _REJECT

        best = self._best_solution
        curr = self._current_solution
        cand = self._candidate_solution

        crit = self._acceptance

        if crit(self._rnd_state, best, curr, cand):  # accept candidate
            w_idx = _BETTER if cand.objective() < curr.objective() else _ACCEPT
            curr = copy.deepcopy(cand)
            self._current_solution = curr

        if cand.objective() < best.objective():  # candidate is new best
            # print(f"New best with objective {cand.objective():.2f}.")
            best = copy.deepcopy(cand)
            self._best_solution = best

            if self._on_best:
                cand = copy.deepcopy(self._on_best(best, self._rnd_state))
                self._candidate_solution = cand

            return best, cand, _BEST

        return best, curr, w_idx
