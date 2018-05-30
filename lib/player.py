import colors
from shapes import *
from util import *

class Player(object):
    """
    Manage the status of the player
    """
    def __init__(self, start_x, start_y, actions=None):
        super(Player, self).__init__()

        # player info
        self.X = start_x
        self.Y = start_y
        self.WIDTH = 10
        self.HEIGHT = 20

        self.INIT_SPEED = 2.0
        self.ACCELERATION = 0.05
        self.MOVE_SPEED = 2.0

        # the height to ground
        self.MAX_HEIGHT = 40
        self.curr_height = 0
        self.on_jump = False
        self.curr_speed = 0.0

        # pre-defined action list
        self.actions = actions
        self.pos_counter = 0

    def jump(self):
        if not self.on_jump:
            self.on_jump = True
            self.curr_speed = self.INIT_SPEED

    def move(self, direction):
        if direction == "left":
            self.X -= self.MOVE_SPEED
        else:
            self.X += self.MOVE_SPEED

    def update(self):
        self.pos_counter += 1
        if self.actions is not None:
            if in_sorted(self.pos_counter, self.actions):
                self.jump()

        if self.on_jump:
            self.curr_height += self.curr_speed
            self.curr_speed -= self.ACCELERATION

            if self.curr_height < 0:
                self.curr_height = 0
                self.on_jump = False

    def is_jumping(self):
        return bool(self.curr_height)

    def get_pos(self):
        return self.X, self.Y

    def get_shapes(self):
        x = self.X
        y = self.Y - self.HEIGHT - self.curr_height
        player_shape = Rectangle(colors.GREEN, x, y, self.WIDTH, self.HEIGHT)
        return [player_shape]
