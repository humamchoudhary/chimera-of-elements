import pygame
import sys


class Scene:
    def __init__(self, screen_size):
        self.entities = []
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((screen_size), pygame.HWSURFACE | pygame.DOUBLEBUF)
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.handle_events(event)

    def pre_run(self):
        pass

    def run(self, fps):
        self.pre_run()
        while True:
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(fps)

    def draw(self):
        # for entity in self.entities:
        #     entity.draw(self.screen, camera)
        pass

    def handle_events(self, event):
        pass
