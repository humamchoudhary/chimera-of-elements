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
        self.zoom = 0.8
        self.cam_surface = pygame.Surface(
            (size[0]*self.zoom, size[1]*self.zoom))
        self.org_size = size
        self.cam_pos = (0, 0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEWHEEL:
                if event.y == -1:
                    self.zoom = min(2, self.zoom * 1.1)

                if event.y == 1:
                    self.zoom = max(0.5, self.zoom / 1.1)

    def update(self, fps=60):
        # self.win.fill(self.bg)

        self.cam_surface = pygame.Surface((self.org_size[
            0]*self.zoom, self.org_size[1]*self.zoom))
        pygame.display.update()
        self.clock.tick(fps)

    def draw(self):

        self.win.fill(self.bg)
