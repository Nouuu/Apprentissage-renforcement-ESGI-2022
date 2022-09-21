import arcade

from env import *


class MazeWindow(arcade.Window):
    def __init__(self, environment):
        super().__init__(environment.width * SPRITE_SIZE,
                         environment.height * SPRITE_SIZE,
                         'ESGI Maze')
