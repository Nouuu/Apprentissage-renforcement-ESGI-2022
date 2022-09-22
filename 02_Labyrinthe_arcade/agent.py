import pickle
from random import uniform, choice

from conf import *
from environment import Environment


class Agent:
    def __init__(self,
                 env: Environment,
                 alpha: float = 1,
                 gamma: float = 0.3,
                 exploration: float = 1,
                 min_exploration: float = 0,
                 cooling_rate: float = 0.999
                 ):
        self.__env = env
        self.reset(False)
        self.__init_qtable()
        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__min_exploration = min_exploration
        self.__cooling_rate = cooling_rate
        self.__history = []

    def reset(self, store_history: bool = True):
        if store_history:
            self.__history.append(self.__score)
        self.__score = 0
        self.__state = self.__env.start_state

    def __init_qtable(self):
        self.__qtable = {}
        for state in self.__env.states:
            self.__qtable[state] = {}
            for action in ACTIONS:
                self.__qtable[state][action] = 0

    def step(self):
        action = self.__best_action()
        reward, state = self.__env.do(self.__state, action)

        max_q = max(self.__qtable[state].values())
        self.__qtable[self.__state][action] += \
            self.__alpha * (reward + self.__gamma * max_q - self.__qtable[self.__state][action])

        self.__state = state
        self.__score += reward
        return action, reward

    def __best_action(self):
        if uniform(0, 1) < self.__exploration:
            self.__exploration *= max(self.__cooling_rate * self.__exploration, self.__min_exploration)
            return choice(ACTIONS)

        actions = self.__qtable[self.__state]
        return max(actions, key=actions.get)

    def learn(self, iterations: int = 1000):
        for i in range(1, iterations + 1):
            if i % (iterations / 10) == 0:
                print(f'Iteration {i}, Score : {self.__score}, E-greedy : {"{:.2f}".format(self.exploration * 100)}%')
            self.reset(store_history=False if i == 1 else True)
            while self.state != self.__env.goal_state:
                self.step()

    def save(self, filename: str):
        with open(filename, 'wb') as file:
            pickle.dump(self.__qtable, file)

    def load(self, filename: str):
        with open(filename, 'rb') as file:
            self.__qtable = pickle.load(file)

    def heat(self):
        self.__exploration = 1

    @property
    def state(self):
        return self.__state

    @property
    def score(self):
        return self.__score

    @property
    def env(self):
        return self.__env

    @property
    def exploration(self):
        return self.__exploration

    @property
    def history(self):
        return self.__history

    def __repr__(self) -> str:
        return str(self.__qtable)
