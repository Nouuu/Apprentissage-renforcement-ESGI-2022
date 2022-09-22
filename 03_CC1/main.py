import os

import arcade

from agent import Agent
from conf import *
from environment import Environment
from plt_exporter import extract_history
from window import MazeWindow


def run(
        brickwalls: bool = False,
        alpha: float = 0.8,
        gamma: float = 0.3,
        exploration: float = 1,
        min_exploration: float = 0.02,
        cooling_rate: float = 0.99,
        nb_learn: int = 20,
        save_state: bool = True,
        display_game: bool = True,
        show_graph: bool = True
):
    environment = Environment(MAZE, brickwalls=brickwalls)
    agent = Agent(
        environment,
        alpha=alpha,
        gamma=gamma,
        exploration=exploration,
        min_exploration=min_exploration,
        cooling_rate=cooling_rate
    )

    if save_state and os.path.exists(FILE_QTABLE):
        agent.load(FILE_QTABLE)

    if nb_learn > 0:
        agent.learn(nb_learn)

    if display_game:
        windows = MazeWindow(agent, True)
        windows.setup()
        arcade.run()

    if save_state:
        agent.save(FILE_QTABLE)

    if show_graph:
        extract_history(agent.history)


if __name__ == "__main__":
    run(
        nb_learn=100,
        brickwalls=False,
        display_game=False,
        save_state=False
    )
