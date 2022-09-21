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

    print(agent.state)

    windows = MazeWindow(agent)
    windows.setup()
    arcade.run()

    # for i in range(100):
    #     steps, score = agent.play()
    #     # environment.print(agent)
    #     print('Steps : ', steps, 'Score : ', score)
    # agent.play(True)
