import pygame
import random
import colors
from shapes import *
from player import Player

class Field(object):
    '''
    Class for maintaining the current field state
    '''
    def __init__(self, screen_width, screen_height, obstacle_pos=None, player_actions=None):
        super(Field, self).__init__()

        # constants
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.GROUND_Y = 200
        self.BLOCK_WIDTH = 10
        self.BLOCK_HEIGHT = 20
        self.MAX_STEP = 400000

        # init obstacle positions
        if obstacle_pos is None:
            self.obstacle_pos = [random.randint(i * 200, (i + 1) * 200) for i in range(2000)]
        else:
            self.obstacle_pos = obstacle_pos

        self.obstacle_pos.sort()
        self.curr_obstacles = []
        self.pos_counter = 0

        # player
        self.PLAYER_X = self.SCREEN_WIDTH * 0.2
        self.player = Player(self.PLAYER_X, self.GROUND_Y, actions=player_actions)

    def _in_sorted(self, elem, sorted_list):
        """Check whether elem is in the sorted list"""
        for i in sorted_list:
            if elem == i:
                return True
            elif elem > i:
                return False
        return False

    def update(self):
        """Method to be called when the game frame is updated"""
        self.pos_counter += 1
        if self._in_sorted(self.pos_counter, self.obstacle_pos):
            new_obs = Rectangle(colors.WHITE, self.SCREEN_WIDTH,
                                self.GROUND_Y - self.BLOCK_HEIGHT, self.BLOCK_WIDTH,
                                self.BLOCK_HEIGHT)
            self.curr_obstacles.append(new_obs)

        # increment all obstacle positions by 1
        for obs in self.curr_obstacles:
            obs.x -= 1

        # delete out of range positions
        if self.curr_obstacles and self.curr_obstacles[0].x < -self.BLOCK_WIDTH:
            del self.curr_obstacles[0]

        self.player.update()

    def get_block_size(self):
        return self.BLOCK_WIDTH, self.BLOCK_HEIGHT

    def get_obstacles(self):
        """Get a list of coordinates for obstacles"""
        return self.curr_obstacles

    def get_shapes(self):
        shapes = []

        # add a horizontal line for the ground
        shapes.append(Line(colors.WHITE, (0, self.GROUND_Y), (self.SCREEN_WIDTH, self.GROUND_Y), width=3))

        shapes += self.curr_obstacles
        shapes += self.player.get_shapes()

        return shapes

    def jump(self):
        self.player.jump()

    def check_is_over(self):
        player_shape = self.player.get_shapes()[0]
        player_rect = player_shape.to_pygame_rect()

        for obs in self.curr_obstacles:
            obstacle_rect = obs.to_pygame_rect()
            if obstacle_rect.colliderect(player_rect):
                return True
        return False

    def quick_play(self):
        score = 0.0
        while self.pos_counter < self.MAX_STEP:
            self.update()
            if self.check_is_over():
                return score
            else:
                score += 0.1
        return score
