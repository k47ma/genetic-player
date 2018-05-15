import pygame
import random

class Game:
    def __init__(self):
        self._done = False
        self.SCREEN_WIDTH = 640
        self.SCREEN_HEIGHT = 400
        self.BLOCK_WIDTH = 10
        self.BLOCK_HEIGHT = 20

        # init pygame        
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.FRAME_RATE = 60
        self.clock = pygame.time.Clock()

        # init obstacle positions
        self.obstacle_pos = [random.randint(1, 1000) for i in range(20)]
        self.obstacle_pos.sort()
        self.curr_obstacles = []
        self.pos_counter = 0
        
        # some useful constants
        self.COLOR_BLACK = (0, 0, 0)
        self.COLOR_WHITE = (255, 255, 255)
        self.COLOR_BLUE = (0, 120, 255)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._done = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q] or pressed[pygame.K_ESCAPE]: 
            self._done = True

    def update_screen(self):
        self.screen.fill(self.COLOR_BLACK)

        self._draw_obstacles()

        pygame.display.flip()
        self.clock.tick(self.FRAME_RATE)

    def on_update(self):
        self.pos_counter += 1
        if self.pos_counter in self.obstacle_pos:
            self.curr_obstacles.append(0)
        if self.pos_counter == 1000:
            self.pos_counter = 0

        # increment all obstacle positions by 1
        for ind in range(len(self.curr_obstacles)):
            self.curr_obstacles[ind] += 1

        # delete out of range positions
        if self.curr_obstacles and self.curr_obstacles[0] > self.SCREEN_WIDTH + self.BLOCK_WIDTH:
            del self.curr_obstacles[0]
        
    def start(self):
        while not self._done:
            self.handle_events()
            self.update_screen()
            self.on_update()

    def _draw_obstacles(self):
        pygame.draw.line(self.screen, self.COLOR_WHITE, (0, 200), (640, 200), 3)
        
        for obs in self.curr_obstacles:
            pygame.draw.rect(self.screen, self.COLOR_WHITE, (640 - obs, 200 - self.BLOCK_HEIGHT, self.BLOCK_WIDTH, self.BLOCK_HEIGHT))

if __name__ == '__main__':
    game = Game()
    game.start()
