import logging
import numpy as np

from .WeightScheme import WeightScheme
from typing import List

logger = logging.getLogger(__name__)

class SegmentedWeights(WeightScheme):
    def __init__(
        self,
        scores: List[float],
        refinements,
        acceptances,
        seg_decay: float,
        seg_length: int = 100,
    ):
        super().__init__(scores, refinements, acceptances)

        if not (0 <= seg_decay <= 1):
            raise ValueError("seg_decay outside [0, 1] not understood.")

        if seg_length < 1:
            raise ValueError("seg_length < 1 not understood.")

        self._seg_decay = seg_decay
        self._seg_length = seg_length
        self._iter_refinement = 0
        self._iter_acceptance = 0

        self._reset_segment_weights()

    def select_refinement(self, rnd_state):
        self._iter_refinement += 1

        if self._iter_refinement % self._seg_length == 0:
    
            self._refinement_weights *= self._seg_decay
            self._refinement_weights += (1 - self._seg_decay) * self._refinement_seg_weights

            self._reset_segment_weights()

        return super().select_refinement(rnd_state)

    def select_acceptance(self, rnd_state):
        self._iter_acceptance += 1

        if self._iter_acceptance % self._seg_length == 0:

            self._acceptance_weights *= self._seg_decay
            self._acceptance_weights += (1 - self._seg_decay) * self._acceptance_seg_weights

            self._reset_segment_weights()

        return super().select_acceptance(rnd_state)

    def update_weights(self, refinement_indexes, acceptance_idx, s_idx):
        for refinement_idx in refinement_indexes:
            self._refinement_seg_weights[refinement_idx] += self._scores[s_idx]
        # TODO: definir como será realizada a atualização dos pesos dos critérios de aceitação. 
        # Solução candidata melhor que a global: 0
        # Solução candidata melhor do que a atual: 0
        # Solução candidata pior que a atual e aceita pelo critério: 
        # Solução candidata pior que a atual e rejeitada pelo critério: 
        # self._acceptance_seg_weights[acceptance_idx] += self._scores[s_idx]

    def _reset_segment_weights(self):
        self._refinement_seg_weights = np.zeros_like(self._refinement_weights)
        self._acceptance_seg_weights = np.zeros_like(self._acceptance_weights)
