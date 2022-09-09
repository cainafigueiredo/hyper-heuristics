from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import Axes, Figure

from alns.State import State
from alns.Statistics import Statistics


class Result:
    """
    Stores ALNS results. An instance of this class is returned once the
    algorithm completes.

    Parameters
    ----------
    best
        The best state observed during the entire iteration.
    statistics
        Statistics collected during iteration.
    """

    def __init__(self, best: State, statistics: Statistics):
        self._best = best
        self._statistics = statistics

    @property
    def best_state(self) -> State:
        """
        The best state observed during the entire iteration.
        """
        return self._best

    @property
    def statistics(self) -> Statistics:
        """
        The statistics object populated during iteration.
        """
        return self._statistics

    @property
    def refinement_weights(self) -> Statistics:
        return self._statistics.refinement_weights

    @property
    def objectives(self) -> Statistics:
        return self._statistics.objectives

    def plot_objectives(
        self,
        ax: Optional[Axes] = None,
        title: Optional[str] = None,
        optimum: int = None,
        **kwargs: Dict[str, Any]
    ):
        """
        Plots the collected objective values at each iteration.

        Parameters
        ----------
        ax
            Optional axes argument. If not passed, a new figure and axes are
            constructed.
        title
            Optional title argument. When not passed, a default is set.
        kwargs
            Optional arguments passed to ``ax.plot``.
        """
        if ax is None:
            _, ax = plt.subplots()

        if title is None:
            title = "Objective value at each iteration"

        # First call is current solution objectives (at each iteration), second
        # call is the best solution found so far (as a running minimum).
        ax.scatter(range(len(self.statistics.objectives)), self.statistics.objectives, s = 12, color = 'k')
        ax.plot(np.maximum.accumulate(self.statistics.objectives), **kwargs)
        if not optimum is None:
            ax.axhline(y = optimum, color = 'r', linestyle = 'dashed')

        ax.set_title(title)
        ax.set_ylabel("Objective value")
        ax.set_xlabel("Iteration (#)")

        yLim = (0,1.05 * np.max(self.statistics.objectives)) if optimum is None else (0,1.05 * optimum)
        ax.set_ylim(*yLim)

        legends = ["Current", "Best"] if optimum is None else ["Current", "Best", "Optimum"]
        ax.legend(legends, loc="lower right")

        plt.draw_if_interactive()