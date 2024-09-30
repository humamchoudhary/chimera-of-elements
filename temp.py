import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
SKY_COLOR = (135, 206, 235)
GROUND_COLOR = (34, 139, 34)

# Block size
BLOCK_SIZE = 16

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side-Scroller with Generated Terrain")

# Generate a simple height map
world_width = 100000  # Adjust as needed
height_map = [random.randint(10, 30) for _ in range(world_width)]

# Camera position
camera_x = 0

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move camera (you can adjust this based on player movement)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        camera_x += 5
    if keys[pygame.K_LEFT]:
        camera_x = max(0, camera_x - 5)

    # Clear the screen
    screen.fill(SKY_COLOR)

    # Calculate the range of blocks to render
    start_block = camera_x // BLOCK_SIZE
    end_block = (camera_x + SCREEN_WIDTH) // BLOCK_SIZE + 1

    # Render visible blocks
    for x in range(start_block, min(end_block, world_width)):
        height = height_map[x]
        for y in range(height):
            block_x = x * BLOCK_SIZE - camera_x
            block_y = SCREEN_HEIGHT - (y + 1) * BLOCK_SIZE
            pygame.draw.rect(screen, GROUND_COLOR,
                             (block_x, block_y, BLOCK_SIZE, BLOCK_SIZE))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
