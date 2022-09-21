from conf import *


class Environment:
    def __init__(self, str_maze: str):
        self.__parse(str_maze)

    def __parse(self, str_maze: str):
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

    def is_forbidden_state(self, state: tuple):
        return state not in self.__states or \
               self.__states[state] in FORBIDDEN_STATES

    def is_wall(self, state: tuple):
        return self.__states[state] == MAZE_WALL

    def is_start(self, state: tuple):
        return self.__states[state] == MAZE_START

    def is_goal(self, state: tuple):
        return self.__states[state] == MAZE_GOAL

    def do(self, state: tuple, action: str):
        move = ACTIONS_MOVES[action]
        new_state = (state[0] + move[0], state[1] + move[1])

        if self.is_forbidden_state(new_state):
            reward = self.__rewards.forbidden_reward
        else:
            state = new_state
            reward = self.__rewards.of(self.__states[new_state])

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
