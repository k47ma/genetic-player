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

        # the height to ground
        self.MAX_HEIGHT = 40
        self.curr_height = 0
        self.direction = None

    def jump(self):
        if self.direction is None:
            self.direction = "up"

    def update(self):
        if self.direction == "up":
            if self.curr_height < self.MAX_HEIGHT:
                self.curr_height += 1
            else:
                self.direction = "down"
        elif self.direction == "down":
            if self.curr_height > 0:
                self.curr_height -= 1
            else:
                self.direction = None

    def get_shapes(self):
        x = self.X
        y = self.Y - self.HEIGHT - self.curr_height
        player_shape = Rectangle(colors.GREEN, x, y, self.WIDTH, self.HEIGHT)
        return [player_shape]
