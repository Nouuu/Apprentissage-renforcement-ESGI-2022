import arcade

from agent import Agent
from conf import *


class MazeWindow(arcade.Window):
    def __init__(self, agent: Agent, auto_play: bool = False):
        super().__init__(agent.env.width * SPRITE_SIZE,
                         agent.env.height * SPRITE_SIZE,
                         '5AL2 Maze')
        self.__agent = agent
        self.__iteration = 1
        self.__auto_play = auto_play

    def setup(self):
        self.__sprites = arcade.SpriteList()
        for state in self.__agent.env.states:
            if self.__agent.env.is_forbidden_state(state):
                sprite = arcade.Sprite(":resources:images/tiles/boxCrate_single.png", 0.5)
                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.__sprites.append(sprite)
            else:
                sprite = arcade.Sprite(":resources:images/tiles/lava.png", 0.5)
                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.__sprites.append(sprite)

        mushroom = arcade.Sprite(":resources:images/tiles/mushroomRed.png", 0.5)
        mushroom.center_x, mushroom.center_y = self.state_to_xy(self.__agent.env.goal_state)
        self.__sprites.append(mushroom)

        self.__agent_sprite = arcade.Sprite(":resources:images/alien/alienBlue_walk1.png", 0.3)
        self.__agent_sprite.center_x, self.__agent_sprite.center_y = self.state_to_xy(self.__agent.state)

    def state_to_xy(self, state: tuple):
        return (state[1] + 0.5) * SPRITE_SIZE, \
               (self.__agent.env.height - state[0] - 0.5) * SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        self.__sprites.draw()
        self.__agent_sprite.draw()

        arcade.draw_text(
            f"Simulation {self.__iteration}, Score : {self.__agent.score}, "
            f"e-greedy : {'{:.2f}'.format(self.__agent.exploration * 100)}%, "
            f"Auto play : {'YES' if self.__auto_play else 'NO'}",
            10, 10, arcade.color.WHITE, 14)

    def new_game(self):
        self.__agent.reset()
        self.__agent_sprite.center_x, self.__agent_sprite.center_y = self.state_to_xy(self.__agent.state)
        self.__iteration += 1

    def on_update(self, delta_time):
        if self.__agent.state != self.__agent.env.goal_state:
            self.__agent.step()
            self.__agent_sprite.center_x = (self.__agent.state[1] + 0.5) * SPRITE_SIZE
            self.__agent_sprite.center_y = (self.__agent.env.height - self.__agent.state[0] - 0.5) * SPRITE_SIZE
        elif self.__auto_play:
            self.new_game()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.new_game()
