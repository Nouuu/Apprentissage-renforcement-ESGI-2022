import pickle
from random import uniform, choice

from conf import *
from environment import Environment


class Agent:
    def __init__(self, env: Environment, alpha: float = 1, gamma: float = 0.3, exploration: float = 1,
                 cooling_rate: float = 0.999):
        self.__env = env
        self.reset()
        self.__init_qtable()
        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate

    def reset(self):
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
            self.__exploration *= self.__cooling_rate
            return choice(ACTIONS)

        actions = self.__qtable[self.__state]
        return max(actions, key=actions.get)

    def learn(self, iterations: int = 1000):
        for _ in range(iterations):
            self.step()
            while self.state != self.__env.goal_state:
                self.step()

    def save(self, filename: str):
        with open(filename, 'wb') as file:
            pickle.dump(self.__qtable, file)

    def load(self, filename: str):
        with open(filename, 'rb') as file:
            self.__qtable = pickle.load(file)

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

    def __repr__(self) -> str:
        return str(self.__qtable)
