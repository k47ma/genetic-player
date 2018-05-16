import pygame
import random
import colors
from shape import *

class Field:
    '''
    Class for maintaining the current field state
    '''
    def __init__(self, screen_width, screen_height):
        # constants
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.BLOCK_WIDTH = 10
        self.BLOCK_HEIGHT = 20

        # init obstacle positions
        self.obstacle_pos = [random.randint(i * 200, (i + 1) * 200) for i in range(20)]
        self.obstacle_pos.sort()
        self.curr_obstacles = []
        self.pos_counter = 0

    def update(self):
        '''
        Method to be called when the game frame is updated
        '''
        self.pos_counter += 1
        if self.pos_counter in self.obstacle_pos:
            self.curr_obstacles.append(0)
        if self.pos_counter == 4000:
            self.pos_counter = 0

        # increment all obstacle positions by 1
        for ind in range(len(self.curr_obstacles)):
            self.curr_obstacles[ind] += 1

        # delete out of range positions
        if self.curr_obstacles and self.curr_obstacles[0] > self.SCREEN_WIDTH + self.BLOCK_WIDTH:
            del self.curr_obstacles[0]

    def get_block_size(self):
        return self.BLOCK_WIDTH, self.BLOCK_HEIGHT

    def get_obstacles(self):
        '''
        Get a list of coordinates for obstacles
        '''
        return self.curr_obstacles

    def get_shapes(self):
        shapes = []
        start_y = 200

        # add a horizontal line for the ground
        shapes.append(Line(colors.WHITE, (0, start_y), (self.SCREEN_WIDTH, start_y), width=3))
        
        for pos in self.curr_obstacles:
            shapes.append(Rectangle(colors.WHITE, self.SCREEN_WIDTH - pos, 
                                    start_y - self.BLOCK_HEIGHT, self.BLOCK_WIDTH, 
                                    self.BLOCK_HEIGHT))
        return shapes
