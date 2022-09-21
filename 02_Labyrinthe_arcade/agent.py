import time

from conf import *
from environment import Environment


class Agent:
    def __init__(self, env: Environment, alpha=1, gamma=0.3):
        self.__env = env
        self.__score = 0
        self.__state = env.start_state
        self.__alpha = alpha
        self.__gamma = gamma
        self.__init_qtable()

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

        self.__score += reward
        self.__state = state
        return action, reward

    def reset(self):
        self.__score = 0
        self.__state = self.__env.start_state

    def __best_action(self):
        actions = self.__qtable[self.__state]
        return max(actions, key=actions.get)

    def play(self, print_maze=False):
        self.reset()
        steps = 0
        while self.state != self.__env.goal_state:
            steps += 1
            self.step()
            if print_maze:
                time.sleep(0.5)
                self.__env.print(self)
        return steps, self.__score

    @property
    def state(self):
        return self.__state

    @property
    def score(self):
        return self.__score

    @property
    def env(self):
        return self.__env

    def __repr__(self) -> str:
        return str(self.__qtable)
