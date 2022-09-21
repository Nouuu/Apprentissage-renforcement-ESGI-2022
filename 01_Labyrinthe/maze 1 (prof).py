# A expérimenter
#
# - Possibilité de traverser des murs
# - Plusieurs solutions au labyrinthe

import time

MAZE = """
#.#############
#     #       #
####  #   #   #
#     #  ### ##
#        #    #
#     #  #    #
#  # #####    #
#     #  ##   #
#        #    #
#             #
#############*#
"""

ACTION_UP = 'U'
ACTION_DOWN = 'D'
ACTION_LEFT = 'L'
ACTION_RIGHT = 'R'
ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]

ACTION_MOVES = { ACTION_UP    : (-1, 0),
                 ACTION_DOWN  : (1, 0),
                 ACTION_LEFT  : (0, -1),
                 ACTION_RIGHT : (0, 1)}

REWARD_DEFAULT = -1

MAZE_START = '.'
MAZE_WALL = '#'
MAZE_GOAL = '*'

class Environment:
    def __init__(self, str_maze):
        self.__parse(str_maze)
        self.__nb_states = len(self.__states)

    def __parse(self, str_maze):
        self.__states = {}        
        for row, line in enumerate(str_maze.strip().splitlines()):
            for col, char in enumerate(line):
                if char == MAZE_START:
                    self.__start = (row, col)
                elif char == MAZE_GOAL:
                    self.__goal = (row, col)
                self.__states[(row, col)] = char

        self.__rows = row + 1
        self.__cols = col + 1 

    def is_forbidden_state(self, state):
        return state not in self.__states \
           or self.__states[state] in [MAZE_WALL, MAZE_START]

    def do(self, state, action):
        move = ACTION_MOVES[action]
        new_state = (state[0] + move[0], state[1] + move[1])
        reward = REWARD_DEFAULT

        if self.is_forbidden_state(new_state):
            reward = -2 * self.__nb_states
        else:
            state = new_state
            if self.__states[state] == MAZE_GOAL:
                reward = self.__nb_states
            
        return reward, state

    def print(self, agent):
        res = ''
        for row in range(self.__rows):
            for col in range(self.__cols):
                state = (row, col)
                if state == agent.state:
                    res += 'A'
                else:
                    res += self.__states[state]
            res += '\n'
        print(res)                 

    @property
    def start(self):
        return self.__start

    @property
    def goal(self):
        return self.__goal

    @property
    def states(self):
        return list(self.__states.keys())

class Agent:
    def __init__(self, env, alpha = 1, gamma = 0.2):
        self.__env = env
        self.reset()
        self.__init_qtable()
        self.__alpha = alpha
        self.__gamma = gamma

    def reset(self):
        self.__state = env.start
        self.__score = 0

    def __init_qtable(self):
        self.__qtable = {}
        for state in self.__env.states:
            self.__qtable[state] = {}
            for action in ACTIONS:
                self.__qtable[state][action] = 0

    def step(self):
        action = self.best_action()
        reward, state = self.__env.do(self.state, action)

        maxQ = max(self.__qtable[state].values())
        self.__qtable[self.state][action] += \
            self.__alpha * (reward + self.__gamma * maxQ - self.__qtable[self.state][action])
        self.__state = state
        self.__score += reward
        return action, reward

    def best_action(self):
        actions = self.__qtable[self.__state]
        return max(actions, key=actions.get)

    @property
    def score(self):
        return self.__score

    @property
    def state(self):
        return self.__state

    def __repr__(self):
        return str(self.__qtable)

if __name__ == '__main__':
    env = Environment(MAZE)
    agent = Agent(env)

    print(agent.state)

    for i in range(60):
        agent.reset()
        iteration = 0
        while agent.state != env.goal:
            action, reward = agent.step()
            #print(iteration, action, reward, agent.state)
            #env.print(agent)
            iteration += 1

        print(i, iteration, agent.score)
        #print(agent)


    agent.reset()
    while agent.state != env.goal:
        action, reward = agent.step()
        env.print(agent)
        time.sleep(1)

