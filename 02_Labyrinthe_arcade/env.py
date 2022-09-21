MAZE = """
#.################
#     #          #
###   #    #     #
#     #    #     #
####       #     #
#  #########  ####
#                #
################*#
"""

ACTION_UP = 'U'
ACTION_DOWN = 'D'
ACTION_LEFT = 'L'
ACTION_RIGHT = 'R'
ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]

ACTIONS_MOVES = {
    ACTION_UP: (-1, 0),
    ACTION_DOWN: (1, 0),
    ACTION_LEFT: (0, -1),
    ACTION_RIGHT: (0, 1),
}

MAZE_START = '.'
MAZE_WALL = '#'
MAZE_GOAL = '*'
MAZE_NONE = ' '
FORBIDDEN_STATES = [MAZE_WALL, MAZE_START]

REWARD_DEFAULT = -1

## Arcade
SPRITE_SIZE = 20

class Rewards:
    def __init__(self, maze_size: int):
        self.__rewards = {
            MAZE_NONE: REWARD_DEFAULT,
            MAZE_WALL: -2 * maze_size,
            MAZE_START: -2 * maze_size,
            MAZE_GOAL: maze_size
        }

    @property
    def get(self):
        return self.__rewards
