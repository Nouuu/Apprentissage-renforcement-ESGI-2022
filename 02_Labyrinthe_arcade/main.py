import time

import arcade

from env import *
from window import MazeWindow


# À expérimenter
#
# - Traverser les murs
# - Plusieurs solutions

class Environment:
    def __init__(self, str_maze: str):
        self.__parse(str_maze)

    def __parse(self, str_maze):
        self.__rewards = Rewards(len(str_maze.strip()))
        self.__states = {}
        for row, line in enumerate(str_maze.strip().splitlines()):
            for col, char in enumerate(line):
                self.__states[(row, col)] = char
                if char == MAZE_START:
                    self.__start_state = (row, col)
                elif char == MAZE_GOAL:
                    self.__goal_state = (row, col)
        self.__rows = len(str_maze.strip().splitlines())
        self.__cols = len(str_maze.strip().splitlines()[0])

    def __is_forbidden_state(self, state: tuple):
        return state not in self.__states or \
               self.__states[state] in FORBIDDEN_STATES

    def do(self, state: tuple, action: str):
        move = ACTIONS_MOVES[action]
        new_state = (state[0] + move[0], state[1] + move[1])
        if self.__is_forbidden_state(new_state):
            reward = self.__rewards.get[MAZE_WALL]
        else:
            state = new_state
            reward = self.__rewards.get[self.__states[new_state]]

        return reward, state

    def print(self, agent):
        # Clear console screen
        res = ""
        for row in range(self.__rows):
            for col in range(self.__cols):
                res += self.__states[(row, col)] if agent.state != (row, col) else 'A'
            res += '\n'
        res += '\n\n'
        print(res)

    @property
    def states(self):
        return list(self.__states.keys())

    @property
    def start_state(self):
        return self.__start_state

    @property
    def goal_state(self):
        return self.__goal_state

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols


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

    def __step(self):
        action = self.__best_action()
        reward, state = self.__env.do(self.__state, action)

        max_q = max(self.__qtable[state].values())
        self.__qtable[self.__state][action] += \
            self.__alpha * (reward + self.__gamma * max_q - self.__qtable[self.__state][action])

        self.__score += reward
        self.__state = state
        return action, reward

    def __reset(self):
        self.__score = 0
        self.__state = self.__env.start_state

    def __best_action(self):
        actions = self.__qtable[self.__state]
        return max(actions, key=actions.get)

    def play(self, print_maze=False):
        self.__reset()
        steps = 0
        while agent.state != environment.goal_state:
            steps += 1
            self.__step()
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

    def __repr__(self) -> str:
        return str(self.__qtable)


if __name__ == "__main__":
    environment = Environment(MAZE)
    agent = Agent(environment)

    print(agent.state)

    windows = MazeWindow(environment)
    arcade.run()

    # for i in range(100):
    #     steps, score = agent.play()
    #     # environment.print(agent)
    #     print('Steps : ', steps, 'Score : ', score)
    # agent.play(True)
