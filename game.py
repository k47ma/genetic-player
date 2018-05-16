import pygame
import random
import colors
from field import Field
from shapes import *

class Game:
    def __init__(self, obstacle_pos=None, auto_mode=False):
        self._done = False
        self.auto_mode = auto_mode
        self.SCREEN_WIDTH = 640
        self.SCREEN_HEIGHT = 400

        # init pygame
        """
        pygame.init()
        pygame.display.set_caption("Game")
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.FRAME_RATE = 60
        self.clock = pygame.time.Clock()
        """

        # field and player objects for each game
        self.obstacle_pos = obstacle_pos
        self.field = None

        self.setup_game()

    def _draw_field(self):
        shapes = self.field.get_shapes()
        for shape in shapes:
            self._draw_shape(shape)

    def setup_game(self):
        self.field = Field(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, obstacle_pos=self.obstacle_pos)

    def is_over(self):
        return self.field.check_is_over()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._done = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q] or pressed[pygame.K_ESCAPE]: 
            self._done = True
        if pressed[pygame.K_SPACE] and not self.auto_mode:
            self.field.jump()
        if pressed[pygame.K_r] and self.is_over():
            self.setup_game()

    def update_screen(self):
        self.screen.fill(colors.BLACK)

        self._draw_field()

        pygame.display.flip()
        self.clock.tick(self.FRAME_RATE)

    def on_update(self):
        """Things to do when frame get updated"""
        self.field.update()

    def get_score(self, actions):
        """Create a new game and quickly finish it to get the score"""
        field = Field(self.SCREEN_WIDTH, self.SCREEN_HEIGHT,
                      obstacle_pos=self.obstacle_pos, player_actions=actions)
        score = field.quick_play()
        return score
        
    def start(self):
        while not self._done:
            self.handle_events()

            if not self.is_over():
                self.update_screen()
                self.on_update()

    def _draw_shape(self, shape):
        if isinstance(shape, Line):
            pygame.draw.line(self.screen, shape.color, shape.start_pos, shape.end_pos, shape.width)
        elif isinstance(shape, Rectangle):
            pygame.draw.rect(self.screen, shape.color, (shape.x, shape.y, shape.width, shape.height))
        else:
            print "[ERROR] Unknown shape type {}!".format(shape.__class__.__name__)

    
if __name__ == '__main__':
    game = Game()
    game.start()
