from entites.base_entity import Entity
import pygame


class Player(Entity):
    def __init__(self, x, y, size):
        super().__init__(x, y-size-20, size, size*2, (0, 0, 255))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.velocity.x -= self.acceleration
        if keys[pygame.K_d]:
            self.velocity.x += self.acceleration
        if keys[pygame.K_w] and self.on_ground:
            self.velocity.y = self.jump_strength
            self.on_ground = False
        if keys[pygame.K_LSHIFT]:
            self.dash()

    def update(self, platforms):
        super().update()
        print(self.rect)
        self.handle_input()
        self.move()
        self.apply_friction()
        self.check_collision(platforms)
