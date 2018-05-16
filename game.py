import pygame
import random
import colors
from field import Field
from shape import *

class Game:
    def __init__(self):
        self._done = False
        self.SCREEN_WIDTH = 640
        self.SCREEN_HEIGHT = 400

        # init pygame        
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.FRAME_RATE = 60
        self.clock = pygame.time.Clock()

        # field and player objects for each game
        self.field = None

        self.setup_game()

    def setup_game(self):
        self.field = Field(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._done = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q] or pressed[pygame.K_ESCAPE]: 
            self._done = True

    def update_screen(self):
        self.screen.fill(colors.BLACK)

        self._draw_field()

        pygame.display.flip()
        self.clock.tick(self.FRAME_RATE)

    def on_update(self):
        '''
        Things to do when frame changed
        '''
        self.field.update()
        
    def start(self):
        while not self._done:
            self.handle_events()
            self.update_screen()
            self.on_update()

    def _draw_shape(self, shape):
        if isinstance(shape, Line):
            pygame.draw.line(self.screen, shape.color, shape.start_pos, shape.end_pos, shape.width)
        elif isinstance(shape, Rectangle):
            pygame.draw.rect(self.screen, shape.color, (shape.x, shape.y, shape.width, shape.height))
        else:
            print "[ERROR] Unknown shape type {}!".format(shape.__class__.__name__)

    def _draw_field(self):
        shapes = self.field.get_shapes()
        for shape in shapes:
            self._draw_shape(shape)

    
if __name__ == '__main__':
    game = Game()
    game.start()
