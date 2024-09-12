import pygame
import sys


class Game:
    def __init__(self, size, title="Chimera Of Elements"):
        pygame.init()
        self.win = pygame.display.set_mode(size)
        # pygame.display.toggle_fullscreen()
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.bg = pygame.Color("black")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self, fps=60):
        # self.win.fill(self.bg)
        pygame.display.update()
        self.clock.tick(fps)

    def draw(self):

        self.win.fill(self.bg)
