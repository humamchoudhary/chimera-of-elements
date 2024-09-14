import pygame


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
        if self.velocity.x > 0:
            self.direction = 1
        elif self.velocity.x < 0:
            self.direction = -1
        self.velocity.y += self.gravity
        self.velocity.y = min(self.velocity.y, 10)  # Terminal velocity

        self.rect.x += int(self.velocity.x)
        self.rect.y += int(self.velocity.y)

    def apply_friction(self):

        if not self.max_speed > 20 and abs(self.velocity.x) > 0:
            self.velocity.x -= min(abs(self.velocity.x),
                                   self.friction) * (1 if self.velocity.x > 0 else -1)

    def dash(self):

        if self.can_dash:
            if self.velocity.x != 0 or int(self.velocity.y) != 0:
                # Dash in the direction of current movement
                dash_vector = self.velocity.normalize() * self.dash_speed
            else:
                # If not moving, dash in the last known direction
                dash_vector = pygame.math.Vector2(
                    self.direction * self.dash_speed, 0)
            print(f"Dash Vector: {dash_vector}")

            self.velocity = dash_vector
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
                self.velocity.x += self.direction * 2
            else:
                self.max_speed = 5

        self.velocity.x = max(-self.max_speed,
                              min(self.velocity.x, self.max_speed))
