import pygame
import sys


class Game:
    def __init__(self, size, title="Chimera Of Elements"):
        pygame.init()
        self.win = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.bg = pygame.Color("black")
        self.zoom = 1
        self.cam_surface = pygame.Surface(
            (size[0] * self.zoom, size[1] * self.zoom))
        self.org_size = size
        self.target = None

        # Camera boundaries (box) inside which player can move freely
        self.camera_bounds = {"left": 200,
                              "top": 100, "right": 200, "bottom": 100}

        # Define camera rect
        l = self.camera_bounds['left']
        t = self.camera_bounds['top']
        w = size[0] - (self.camera_bounds['left'] +
                       self.camera_bounds['right']*2)
        h = size[1] - (self.camera_bounds['top'] +
                       self.camera_bounds['bottom']*2)
        self.camera = pygame.Rect(l, t, w, h)

        self.offset = pygame.Vector2()

    def draw_world(self, objects):

        for obj in objects:
            obj_rect = obj.move(-self.offset.x, -self.offset.y)
            zoomed_rect = pygame.Rect(obj_rect.left * self.zoom, obj_rect.top * self.zoom,
                                      obj_rect.width * self.zoom, obj_rect.height * self.zoom)
            pygame.draw.rect(self.win, (255, 255, 0), zoomed_rect)

    def update_camera(self):
        # Check if player moves outside the left boundary
        if self.target.rect.left < self.camera.left:
            self.camera.left = self.target.rect.left

        # Check if player moves outside the right boundary
        if self.target.rect.right > self.camera.right:
            print("righ out")
            self.camera.right = self.target.rect.right

        # Check if player moves outside the top boundary
        if self.target.rect.top < self.camera.top:
            self.camera.top = self.target.rect.top

        # Check if player moves outside the bottom boundary
        if self.target.rect.bottom > self.camera.bottom:
            self.camera.bottom = self.target.rect.bottom

        # Set the camera offset to adjust rendering positions
        self.offset.x = -(self.camera.centerx - self.org_size[0]//2)
        self.offset.y = -(self.camera.centery - self.org_size[1]//2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Adjust zoom based on mouse wheel
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:  # Zoom in
                    self.zoom = min(2.0, self.zoom * 1.1)
                elif event.y < 0:  # Zoom out
                    self.zoom = max(0.5, self.zoom / 1.1)

                # Adjust camera and surface size based on zoom level
                new_width = self.org_size[0] * self.zoom
                new_height = self.org_size[1] * self.zoom
                self.camera.width = new_width - \
                    (self.camera_bounds['left'] + self.camera_bounds['right'])
                self.camera.height = new_height - \
                    (self.camera_bounds['top'] + self.camera_bounds['bottom'])

    def update(self, fps=60):
        # self.win.fill(self.bg)

        # self.cam_surface = pygame.Surface((self.org_size[
        #     0]*self.zoom, self.org_size[1]*self.zoom))
        self.update_camera()
        pygame.display.update()

        self.clock.tick(fps)

    def draw(self):
        self.win.fill(self.bg)

    def draw_cam(self):
        pygame.draw.rect(self.win, "red", self.camera, 5)
