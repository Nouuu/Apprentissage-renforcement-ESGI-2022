import os

import arcade

from agent import Agent
from conf import *
from environment import Environment
from plt_exporter import PLTExporter
from window import MazeWindow

# À expérimenter
#
# - Traverser les murs
# - Plusieurs solutions

if __name__ == "__main__":
    environment = Environment(MAZE, brickwalls=True)
    agent = Agent(environment, alpha=1, gamma=0.3, cooling_rate=0.99)

    if os.path.exists(FILE_QTABLE):
        agent.load(FILE_QTABLE)

    agent.learn(30)

    windows = MazeWindow(agent, True)
    windows.setup()
    arcade.run()

    agent.save(FILE_QTABLE)
    PLTExporter.extract_history(agent.history)
