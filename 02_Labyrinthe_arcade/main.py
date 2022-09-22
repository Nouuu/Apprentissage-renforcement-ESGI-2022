import os

import arcade

from agent import Agent
from conf import *
from environment import Environment
from plt_exporter import extract_history
from window import MazeWindow

# À expérimenter
#
# - Traverser les murs
# - Plusieurs solutions

if __name__ == "__main__":
    environment = Environment(MAZE)
    agent = Agent(
        environment,
        alpha=0.8,
        gamma=0.8,
        exploration=1,
        min_exploration=0,
        cooling_rate=0.99
    )

    if os.path.exists(FILE_QTABLE):
        agent.load(FILE_QTABLE)

    print(len(environment.states))

    agent.learn(30)

    windows = MazeWindow(agent, True)
    windows.setup()
    arcade.run()

    agent.save(FILE_QTABLE)
    extract_history(agent.history)
