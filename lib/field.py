import random
import colors
from shapes import *
from util import *
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
        self.MAX_STEP = 40000
        self.PENALTY = 10.0

        # init obstacle positions
        if obstacle_pos is None:
            self.obstacle_pos = [random.randint(i * 200, (i + 1) * 200) for i in range(200)]
        else:
            self.obstacle_pos = obstacle_pos

        self.curr_obstacles = []
        self.pos_counter = 0
        self.score = 0.0

        # player
        self.PLAYER_X = self.SCREEN_WIDTH * 0.2
        self.player = Player(self.PLAYER_X, self.GROUND_Y, actions=player_actions)

        # boolean for penalty
        self.new_jump = False
        self.invalid_jump = False

    def update(self):
        """Method to be called when the game frame is updated"""
        self.pos_counter += 1
        self.score += 0.1

        if in_sorted(self.pos_counter, self.obstacle_pos):
            new_obs = Rectangle(colors.WHITE, self.SCREEN_WIDTH,
                                self.GROUND_Y - self.BLOCK_HEIGHT, self.BLOCK_WIDTH,
                                self.BLOCK_HEIGHT)
            self.curr_obstacles.append(new_obs)

        # decrement all obstacle positions by 1
        for obs in self.curr_obstacles:
            obs.x -= 1

        # calculate penalty
        if self.player.is_jumping() and not self.new_jump:
            self.new_jump = True
            self.invalid_jump = True

        if self.player.get_pos()[0] in [obs.x for obs in self.curr_obstacles]:
            self.invalid_jump = False

        if not self.player.is_jumping():
            self.new_jump = False
            if self.invalid_jump:
                self.score -= self.PENALTY
            self.invalid_jump = False

        # delete out of range positions
        if self.curr_obstacles and self.curr_obstacles[0].x < -self.BLOCK_WIDTH:
            del self.curr_obstacles[0]

        self.player.update()

    def get_block_size(self):
        return self.BLOCK_WIDTH, self.BLOCK_HEIGHT

    def get_obstacles(self):
        """Get a list of coordinates for obstacles"""
        return self.curr_obstacles

    def get_score(self):
        return self.score

    def get_shapes(self):
        shapes = []

        # add a horizontal line for the ground
        shapes.append(Line(colors.WHITE, (0, self.GROUND_Y), (self.SCREEN_WIDTH, self.GROUND_Y), width=3))

        shapes += self.curr_obstacles
        shapes += self.player.get_shapes()

        return shapes

    def jump(self):
        self.player.jump()

    def move(self, direction):
        player_rect = self.player.get_shapes()[0]
        if direction == "left" and player_rect.x > 0:
            self.player.move("left")
        elif direction == "right" and player_rect.x < self.SCREEN_WIDTH - player_rect.width:
            self.player.move("right")

    def check_is_over(self):
        player_shape = self.player.get_shapes()[0]
        player_rect = player_shape.to_pygame_rect()

        for obs in self.curr_obstacles:
            obstacle_rect = obs.to_pygame_rect()
            if obstacle_rect.colliderect(player_rect):
                return True
        return False

    def quick_play(self):
        """Run the game without stop and return the score"""
        while self.pos_counter < self.MAX_STEP:
            if self.check_is_over():
                return self.score
            self.update()
        return self.score
