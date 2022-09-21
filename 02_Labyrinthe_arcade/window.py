import arcade

from conf import *


class MazeWindow(arcade.Window):
    def __init__(self, agent):
        super().__init__(agent.env.width * SPRITE_SIZE,
                         agent.env.height * SPRITE_SIZE,
                         '5AL2 Maze')
        self.__agent = agent

    def setup(self):
        self.__walls = arcade.SpriteList()
        for state in self.__agent.env.states:
            if self.__agent.env.is_forbidden_state(state):
                sprite = arcade.Sprite(":resources:images/tiles/boxCrate_single.png", 0.5)
                sprite.center_x = (state[1] + 0.5) * SPRITE_SIZE
                sprite.center_y = (self.__agent.env.height - state[0] - 0.5) * SPRITE_SIZE
                self.__walls.append(sprite)

        self.__goal = arcade.Sprite(":resources:images/tiles/mushroomRed.png", 0.5)
        self.__goal.center_x = (self.__agent.env.goal_state[1] + 0.5) * SPRITE_SIZE
        self.__goal.center_y = (self.__agent.env.height - self.__agent.env.goal_state[0] - 0.5) * SPRITE_SIZE

        self.__alien = arcade.Sprite(":resources:images/alien/alienBlue_walk1.png", 0.3)
        self.__alien.center_x = (self.__agent.state[1] + 0.5) * SPRITE_SIZE
        self.__alien.center_y = (self.__agent.env.height - self.__agent.state[0] - 0.5) * SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        self.__walls.draw()
        self.__goal.draw()
        self.__alien.draw()

    def on_update(self, delta_time):
        if self.__agent.state != self.__agent.env.goal_state:
            self.__agent.step()
            self.__alien.center_x = (self.__agent.state[1] + 0.5) * SPRITE_SIZE
            self.__alien.center_y = (self.__agent.env.height - self.__agent.state[0] - 0.5) * SPRITE_SIZE
        else:
            self.__agent.reset()
