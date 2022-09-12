import numpy as np
import time

from gym import Env, spaces
from src.HyperHeuristic import HyperHeuristic

class HyperHeuristicEnv(Env):
    def __init__(
        self, 
        hyperHeuristic: HyperHeuristic, 
        instanceGenerator, 
        rnd_state: np.random.RandomState = np.random.RandomState(0)
    ):
        super().__init__()

        self._hyperHeuristic = hyperHeuristic
        self._instanceGenerator = instanceGenerator

        self.observation_space = spaces.Box(low = np.array([1, 1]), high = np.array([6, 3]), dtype = np.int16)
        self._observation_space_dim = self.observation_space.high - self.observation_space.low + 1
        self.observation_space.n = np.multiply.reduce(self._observation_space_dim, initial = 1)

        self.action_space = spaces.Discrete(len(self._hyperHeuristic.refinement))
        
        self._action_to_heuristic_map = {actionID: self._hyperHeuristic.refinement[actionID][0] for actionID in range(self.action_space.n)}

        self._rnd_state = rnd_state

        self._last_episode_fo = None # Setado quando done == True ou na primeira instância vista
        self._f_new = [] # Resetado quando o episódio acaba e modificado no reset e no step

        self._epochs = [] # Tempo, solução (e.g., fitness)
        self._epoch_iterations_fitness = []
        self._noImprovements = 0

        self._epoch_start = None
        self._epoch_end = None

    def get_running_time(self):
        if self._epoch_end is None or self._epoch_start is None:
            raise ValueError("Start and end time can not be None")
        return self._epoch_end - self._epoch_start

    def encode_state(self, state):
        nValuesInState = (self.observation_space.high - self.observation_space.low) + 1
        stateID = 0
        multFactor = np.multiply.reduce(nValuesInState, initial = 1)
        for i, n in enumerate(nValuesInState):
            multFactor = multFactor/nValuesInState[i]
            stateID += (state[i]-self.observation_space.low[i])*multFactor

        return int(stateID)

    def get_heuristic_from_action(self, action):
        assert action >= 0 and action < self.action_space.n, "Action does not exist"

        return self._action_to_heuristic_map[action]

    def get_state(self):
        # No improvements
        noImprovementsState = -1
        if self._noImprovements < 10:
            noImprovementsState = 1
        elif self._noImprovements < 100:
            noImprovementsState = 2
        else:
            noImprovementsState = 3

        median_f_new = np.median(self._f_new)
        relChange = (median_f_new - self._last_episode_fo)/median_f_new
        
        relChangeState = -1
        # Median(f_new) is decreasing in the epoch (in a maximization problem)
        if relChange < -0.67:
            relChangeState = 0

        elif relChange < -0.33:
            relChangeState = 1

        elif relChange < 0:
            relChangeState = 2

        # Median(f_new) is increasing in the epoch (in a maximization problem)
        elif relChange < 0.33:
            relChangeState = 3

        elif relChange < 0.67:
            relChangeState = 4

        else:
            relChangeState = 5

        return self.encode_state([noImprovementsState, relChangeState])

    def reset(self, instance = None):
        self._epoch_start = time.time()

        self._f_new = []
        self._epoch_iterations_fitness = []

        # Gerar uma nova instância
        if instance is None:
            instance_name, instance = self._instanceGenerator.__next__()

        # Encontrar uma solução inicial
        initialSolution = self._hyperHeuristic.initial_solution(instance, None, self._rnd_state)
        objective = initialSolution.objective(isMinimizing = False)
        self._f_new.append(objective)
        self._epoch_iterations_fitness.append(objective)

        if self._last_episode_fo == None:
            self._last_episode_fo = initialSolution.objective(isMinimizing = False)

        # Determina o estado atual
        state = self.get_state()

        # Retorna o estado atual
        return state

    def step(self, action):
        # Dada a solução corrente, executa action (LLH escolhida)
        heuristicName = self._action_to_heuristic_map[action]
        # print(f"Running {heuristicName}")
        currentSolution = self._hyperHeuristic.current_solution
        candidateSolution = self._hyperHeuristic.refine(currentSolution, heuristicName)
        objective = candidateSolution.objective(isMinimizing = False)
        self._f_new.append(objective)

        # Aceitação
        bestSolution, currentSolution, rewardStatus = self._hyperHeuristic.eval_cand()
        self._epoch_iterations_fitness.append(currentSolution.objective(isMinimizing = False))

        # Determina o próximo estado
        if rewardStatus in [0,1]: # BEST (new global solution) or BETTER (better than the current solution)
            self._noImprovements = 0
        else: # ACCEPT or REJECT (both cases comprise worst solutions)
            self._noImprovements += 1

        next_state = self.get_state()

        # Aplica a recompensa
        reward = self._hyperHeuristic.get_reward(rewardStatus)

        # Determinar se done = True ou done = False
        done = self._hyperHeuristic.eval_stop(self._rnd_state, bestSolution, currentSolution)

        # Atualiza solução do último episódio
        if done == True:
            self._last_episode_fo = currentSolution.objective(isMinimizing = False)
            self._epoch_end = time.time()
            self._epochs.append([self._epoch_iterations_fitness, self._epoch_end - self._epoch_start])

        # Retorna (next_state, reward, done, info) 
        return next_state, reward, done, {}

    def render(self):
        # Printa o estado atual
        pass