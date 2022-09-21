import os

import arcade

from agent import Agent
from conf import *
from environment import Environment
from window import MazeWindow

# À expérimenter
#
# - Traverser les murs
# - Plusieurs solutions

if __name__ == "__main__":
    environment = Environment(MAZE)
    agent = Agent(environment)

    if os.path.exists(FILE_QTABLE):
        agent.load(FILE_QTABLE)

    print(len(environment.states))

    windows = MazeWindow(agent, True)
    windows.setup()
    arcade.run()

    agent.save(FILE_QTABLE)

    print(agent.score)
