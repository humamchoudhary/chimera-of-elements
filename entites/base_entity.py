import pygame


# class Entity:
#     def __init__(self, name=None, x=0, y=0, w=10, h=20, type=None, health=20, attack=1, speed=1, sprite=None, momentum=1.2):
#         self.name = name
#         self.type = type
#         self.health = health
#         self.attack = attack
#         self.speed = speed
#         self.x = x
#         self.y = y
#         self.h, self.w = h, w
#         self.sprite = sprite
#         self.hitbox_color = pygame.Color('red')
#         print(f"{x}-{y}-{w}-{h}")
#         self.momentum = momentum
#         self.hitbox = pygame.Rect(x, y, w, h)
#         self.max_speed = 3
#         self.velocity = pygame.Vector2(0, 0)
#         self.is_falling = True
#         self.collision_sides = {"left": False,
#                                 "right": False, "bottom": False, "top": False}
#
#     def draw(self, window):
#         pygame.draw.rect(window, self.hitbox_color, self.hitbox)
#
#     def move(self):
#         pass
#
#     def update(self):
#         pass
#
#     def collision(self, obj):
#         # self.collision_sides = {"left": False,
#         #                         "right": False, "bottom": False, "top": False}
#
#         if self.hitbox.right > obj.left and self.hitbox.left < obj.left:
#             self.collision_sides["right"] = True
#             self.hitbox.right = obj.left
#             print("right")
#         elif self.hitbox.left < obj.right and self.hitbox.right > obj.right:
#             self.collision_sides["left"] = True
#             self.hitbox.left = obj.right
#             print("left")
#         if self.hitbox.bottom > obj.top and self.hitbox.top < obj.top:
#             self.collision_sides["bottom"] = True
#             # self.hitbox.bottom = obj.top
#             print("bottom")
#         elif self.hitbox.top < obj.bottom and self.hitbox.bottom > obj.bottom:
#             self.collision_sides["top"] = True
#             self.hitbox.top = obj.bottom
#             print("top")


class Entity:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5
        self.acceleration = 1
        self.friction = 0.5
        self.gravity = 0.8
        self.jump_strength = -15
        self.on_ground = False
        self.dash_speed = 30
        self.dash_cooldown = 8
        self.dash_timer = 0
        self.direction = 1
        self.can_dash = True
        self.dash_duration = 0.3

    def move(self):
        self.velocity.y += self.gravity
        self.velocity.y = min(self.velocity.y, 10)  # Terminal velocity

        self.rect.x += int(self.velocity.x)
        self.rect.y += int(self.velocity.y)
        # if self.velocity.x > 0:
        #     self.direction = 1
        # elif self.velocity.x < 0:
        #     self.direction = -1

    def apply_friction(self):
        if abs(self.velocity.x) > 0:
            self.velocity.x -= min(abs(self.velocity.x),
                                   self.friction) * (1 if self.velocity.x > 0 else -1)

    def dash(self):
        if self.can_dash:
            if self.velocity.x and self.velocity.y > 0 or self.velocity.y < 0:

                self.velocity *= self.dash_speed
            else:
                self.velocity.x += self.direction * self.dash_speed
            self.dash_timer = pygame.time.get_ticks()
            self.can_dash = False

    def check_collision(self, objs):
        for obj in objs:
            if self.rect.colliderect(obj):
                if self.velocity.y > 0 and self.rect.bottom > obj.top and self.rect.top < obj.top:
                    self.rect.bottom = obj.top
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0 and self.rect.top < obj.bottom and self.rect.bottom > obj.bottom:
                    self.rect.top = obj.bottom
                    self.velocity.y = 0
                elif self.velocity.x > 0 and self.rect.right > obj.left and self.rect.left < obj.left:
                    self.rect.right = obj.left
                    self.velocity.x = 0
                elif self.velocity.x < 0 and self.rect.left < obj.right and self.rect.right > obj.right:
                    self.rect.left = obj.right
                    self.velocity.x = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def __str__(self):
        ret = ""
        for k, v in self.__dict__.items():
            ret += f"\n {k}: {v} \n"
        return ret

    def update(self):
        cur_time = pygame.time.get_ticks()
        if not self.can_dash:

            if cur_time - self.dash_timer > self.dash_cooldown * 1000:
                self.can_dash = True

            if cur_time - self.dash_timer < self.dash_duration * 1000:
                self.max_speed = 40
                self.velocity.x += 2
            else:
                self.max_speed = 5
