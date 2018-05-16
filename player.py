import colors
from shapes import *

class Player(object):
    '''
    Manage the status of the player
    '''
    def __init__(self, start_x, start_y):
        super(Player, self).__init__()

        # player info
        self.X = start_x
        self.Y = start_y
        self.WIDTH = 10
        self.HEIGHT = 20

        self.INIT_SPEED = 2.0
        self.ACCELERATION = 0.05

        # the height to ground
        self.MAX_HEIGHT = 40
        self.curr_height = 0
        self.on_jump = False
        self.curr_speed = 0.0

    def jump(self):
        if not self.on_jump:
            self.on_jump = True
            self.curr_speed = self.INIT_SPEED

    def update(self):
        if self.on_jump:
            self.curr_height += self.curr_speed
            self.curr_speed -= self.ACCELERATION

            if self.curr_height < 0:
                self.curr_height = 0
                self.on_jump = False

    def get_shapes(self):
        x = self.X
        y = self.Y - self.HEIGHT - self.curr_height
        player_shape = Rectangle(colors.GREEN, x, y, self.WIDTH, self.HEIGHT)
        return [player_shape]
