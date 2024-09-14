from game import Game
from entites import Player
import pygame
DEBUG = True

if __name__ == "__main__":
    winSize = (1920, 1080)
    zoom_state = 0.8
    gameLoop = Game(winSize)
    p = Player(x=60, y=100)

    objects = [pygame.Rect(50, 400, 5000, 100), pygame.Rect(300, 300, 100, 20)]

    while True:
        gameLoop.cam_surface.fill(pygame.Color("black"))
        gameLoop.handle_events()
        gameLoop.draw()
        p.update(objects)

        for i in objects:
            pygame.draw.rect(gameLoop.cam_surface, (255, 255, 0), i)

        p.draw(gameLoop.cam_surface)
        gameLoop.win.blit(pygame.transform.scale(
            gameLoop.cam_surface, winSize), gameLoop.cam_pos)
        gameLoop.update()
