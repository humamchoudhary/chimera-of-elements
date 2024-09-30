# from game import Game
from entites import Player
from Scenes.Game import Game
# import Scenes.Game
import pygame


# if __name__ == "__main__":
#     winSize = (1920, 1080)
#     zoom_state = 0.8
#     gameLoop = Game(winSize)
#     p = Player(x=60, y=100)
#     gameLoop.target = p
#     objects = [pygame.Rect(50, 400, 5000, 100), pygame.Rect(300, 300, 100, 20)]
#
#     while True:
#         gameLoop.cam_surface.fill(pygame.Color("black"))
#         gameLoop.handle_events()
#         gameLoop.draw()
#         p.update(objects)
#         gameLoop.draw_world(objects)
#
#         p.draw(gameLoop.cam_surface, gameLoop.zoom)
#         print(gameLoop.offset)
#         gameLoop.win.blit(pygame.transform.scale(
#             gameLoop.cam_surface, winSize), gameLoop.offset)
#         gameLoop.draw_cam()
#
#         gameLoop.update()
def main():

    pygame.init()
    game_scene = Game((1920, 1080))
    game_scene.run(60)
    pass


if __name__ == "__main__":
    main()
