from game import Game
from entites import Player
import pygame
DEBUG = True

if __name__ == "__main__":
    winSize = (1920, 1080)
    display = pygame.Surface((winSize[0], winSize[1]))
    gameLoop = Game(winSize)
    p = Player(x=60, y=100)

    objects = [pygame.Rect(50, 400, 5000, 100), pygame.Rect(300, 300, 100, 20)]

    while True:
        display.fill(pygame.Color("black"))
        gameLoop.handle_events()
        gameLoop.draw()

        p.update(objects)
        # enemy.update(platforms)

        for i in objects:
            pygame.draw.rect(display, (255, 255, 0), i)

        # p.input()
        # p.move()
        p.draw(display)
        # p.update()
        # test_en.draw(gameLoop.win)
        # test_en.update()
        # pygame.display.flip()
        gameLoop.win.blit(pygame.transform.scale(display, winSize), (0, 0))
        gameLoop.update(20)
