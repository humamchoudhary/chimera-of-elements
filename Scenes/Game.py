import matplotlib.pyplot as plt
import pygame
from Scenes import Scene
from entites import Player
import random
import numpy as np
import cProfile
import pstats
import io
import noise
import multiprocessing
import ctypes
import sys
from PIL import Image


def generate_block_ids_batch(x_start, x_end, y_max_values, world_height, world_width, shared_array_base):
    """
    Generate blocks for a batch of columns based on the height map using shared memory.
    Each process works on a range of x-coordinates.
    """
    # Convert the shared array to a numpy array
    shared_array = np.ctypeslib.as_array(shared_array_base.get_obj())
    shared_array = shared_array.reshape(world_height, world_width)
    print("x_start",x_start)

    for x in range(x_start, x_end):
        y_max = y_max_values[x]
        for y in range(y_max):
            # print("y_max", y_max)
            block_id = generate_block_id(x, y)
            shared_array[y, x] = block_id


def generate_block_id(x, y, scale=0.1, octaves=6, persistence=0.5, lacunarity=2.0, seed=None):
    """
    Generate a block ID using Simplex noise based on x and y coordinates.
    """
    noise_value = noise.pnoise2(x * scale, y * scale, octaves=octaves, persistence=persistence,
                          lacunarity=lacunarity, base=seed if seed is not None else np.random.randint(0, 1000))
    scaled_value = (noise_value + 1) * 6
    return int(np.clip(scaled_value, 0, 12))


def generate_world(world_width, world_height, world_height_map):
    """
    Generate the world using multiprocessing. Each process handles one chunk of columns based on the height map.
    """
    # Create shared memory for the world array
    shared_array_base = multiprocessing.Array(
        ctypes.c_uint8, world_height * world_width)

    # Define the number of processes and the chunk size
    num_processes = multiprocessing.cpu_count()-2
    chunk_size = world_width // num_processes

    # Create and start processes
    processes = []
    for i in range(num_processes):
        x_start = i * chunk_size
        # Ensure the last process covers the remainder
        x_end = (i + 1) * chunk_size if i != num_processes - 1 else world_width
        process = multiprocessing.Process(target=generate_block_ids_batch,
                                          args=(x_start, x_end, world_height_map, world_height, world_width, shared_array_base))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    # Convert the shared array back to a numpy array for further processing
    world = np.ctypeslib.as_array(shared_array_base.get_obj())
    world = world.reshape(world_height, world_width)

    return world


class Perlin:
    def __init__(self, seed, octaves=[], strengths=[], initial_size=100):
        np.random.seed(seed)
        random.seed(seed)
        self.i = 0
        self.octaves = octaves
        self.strengths = strengths
        self.height_map = np.array([])
        self.size = initial_size
        self.base = random.randint(0, 500)

    def generate(self, size):
        x_loc = np.zeros((len(self.octaves), size))
        for j, (octave, s) in enumerate(zip(self.octaves, self.strengths)):
            for k in range(size):
                x_loc[j, k] = noise.pnoise1(
                    (self.i + k) / 100.0, octaves=octave, persistence=s, base=self.base
                )
        x_loc = x_loc.sum(axis=0)
        self.height_map = np.concatenate((self.height_map, x_loc))
        self.i += size
        self.size += size
        return x_loc

    def get_world(self):
        return self.world_height_map

    def plot_world(self):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(15, 5))
        plt.plot(self.world_height_map)
        plt.title("Generated World Noise")
        plt.xlabel("Position")
        plt.ylabel("Height")
        plt.show()


class World_Generator:
    biomes = [
        {
            "name": "Ocean",
            "octaves": [1, 2],
            "strengths": [0.5, 0.25],
            "y": (-1.0, -0.5),
            "strength": 0.6,

        },
        {
            "name": "Beach",
            "octaves": [1, 2],
            "strengths": [0.3, 0.2],
            "y": (-0.3, 0.1),
            "strength": 0.01,
        },
        {
            "name": "Plains",
            "octaves": [1, 1, 1],
            "strengths": [0.1, 0.1, 0.2],
            "y": (-0.4, 0.5),
            "strength": 0.01,
        },
        {
            "name": "Forest",
            "octaves": [2, 3, 4],
            "strengths": [0.5, 0.2, 0.2],
            "y": (0.0, 0.6),
            "strength": 0.1,
        },
        {
            "name": "Taiga",
            "octaves": [2, 3, 5],
            "strengths": [0.2, 0.2, 0.1],
            "y": (0.3, 0.7),
            "strength": 0.05,
        },
        {
            "name": "Swamp",
            "octaves": [1, 2, 4],
            "strengths": [0.3, 0.2, 0.1],
            "y": (-0.2, 0.2),
            "strength": 0.05,
        },
        {
            "name": "Savanna",
            "octaves": [1, 2, 3],
            "strengths": [1, 0.5, 0.25],
            "y": (0.1, 0.5),
            "strength": 0.4,
        },
        {
            "name": "Desert",
            "octaves": [1, 2],
            "strengths": [0.2, 0.2],
            "y": (-0.1, 0.4),
            "strength": 0.1,
        },
        {
            "name": "Badlands",
            "octaves": [3, 4, 5],
            "strengths": [0.7, 0.3, 0.5],
            "y": (0.2, 0.8),
            "strength": 0.6,
        },
        {
            "name": "Jungle",
            "octaves": [3, 5, 7],
            "strengths": [1, 0.7, 0.3],
            "y": (0.0, 0.7),
            "strength": 0.3,
        },
        {
            "name": "Mountains",
            "octaves": [4, 6, 8, 24],
            "strengths": [1, 0.2, 0.4, 0.5],
            "y": (0.8, 1.0),
            "strength": 0.7,
        },
        {
            "name": "Plateaus",
            "octaves": [2, 3],
            "strengths": [0.8, 0.4],
            "y": (0.6, 0.8),
            "strength": 0.01,
        },
        {
            "name": "Tundra",
            "octaves": [2, 3],
            "strengths": [1, 0.5],
            "y": (0.4, 0.8),
            "strength": 0.4,
        },
        {
            "name": "Ice Plains",
            "octaves": [1, 2, 3],
            "strengths": [0.2, 0.1, 0.03],
            "y": (0.8, 0.9),
            "strength": 0.01,
        },
        {
            "name": "Snowy Mountains",
            "octaves": [4, 5, 6],
            "strengths": [0.9, 0.6, 0.3],
            "y": (0.8, 1.0),
            "strength": 0.7,
        },
    ]
    blocks = [
        # Air is present everywhere
        {"name": "grass_block", "id": 1, "max": 200, "min": 50,"color":"green"},
        {"name": "dirt", "id": 2, "max": 200, "min": 0,"color":"brown"},
        {"name": "stone", "id": 3, "max": 200, "min": 0,"color":"gray"},
        {"name": "bedrock", "id": 4, "max": 5, "min": 0,"color":"black"},
        {"name": "sand", "id": 5, "max": 200, "min": 50,"color":"yellow"},
        {"name": "gravel", "id": 6, "max": 200, "min": 0,"color":"gray"},
        {"name": "coal_ore", "id": 7, "max": 120, "min": 5,"color":"black"},
        {"name": "iron_ore", "id": 8, "max": 100, "min": 10,"color":"white"},
        {"name": "gold_ore", "id": 9, "max": 80, "min": 20,"color":"yellow"},
        {"name": "diamond_ore", "id": 10, "max": 60, "min": 5,"color":"blue"},
        {"name": "water", "id": 11, "max": 200, "min": 0,"color":"blue"},
        {"name": "lava", "id": 12, "max": 50, "min": 0,"color":"yellow"},
    ]

    def __init__(self, seed=None):
        self.seed = seed if seed else random.randint(0, 2**32 - 1)
        print(self.seed)
        self.p_biome = Perlin(self.seed, [1, 3, 16, 24], [
                              0.6, 0.2, 0.1, 0.1], 0)
        self.p_terrain = Perlin(self.seed,)
        self.chunk_size = 32
        self.world_size = 500  # in Chunks
        self.p_world = Perlin(self.seed)
        self.chunk_biome_map = self.generate_chunk_map(self.world_size)
        self.chunk_biome_map = np.concatenate(
            (self.chunk_biome_map, self.generate_chunk_map(self.world_size)), axis=0
        )
        # print(len(self.chunk_biome_map))
        self.world_height_map = np.array([],dtype=np.uint8)
        self.biome_map = []
        self.generate_world()
        self.world_height_map =self.world_height_map.astype(np.uint8) 
        

        max_height = int(np.max(self.world_height_map))
        self.terrain = generate_world(max_height + 5, len(self.world_height_map), self.world_height_map)
        self.terrain = np.flipud(self.terrain)

             
#         print([
#     [
#         (x, y, id)  # x-coordinate, y-coordinate, id value
#         for x, id in enumerate(row[:10])  # Iterate over each element in the row with its x index
#     ]
#     for y, row in enumerate(self.terrain)  # Iterate over each row with its y index
# ])
        # Image.fromarray(self.terrain).save("temp.png")



    def generate_chunk(self, size, min=-1, max=1):
        noise = self.p_world.generate(size)
        noise = np.round(noise, 2)
        noise = self.scale(noise, min, max)
        return noise

    def generate_world(self):
        for i, height in np.ndenumerate(self.chunk_biome_map):
            possible_biomes = [
                biome
                for biome in self.biomes
                if biome["y"][0] <= height <= biome["y"][1]
            ]
            if possible_biomes:
                chosen_biome = random.choice(possible_biomes)
                self.biome_map.append(chosen_biome["name"])
            else:
                chosen_biome = (
                    self.biomes[
                        next(
                            index
                            for index, item in enumerate(self.biomes)
                            if isinstance(item, dict)
                            and item.get("name") == self.biome_map[i[0] - 1]
                        )
                    ]
                    if i[0] - 1 >= 0
                    else self.biomes[
                        next(
                            index
                            for index, item in enumerate(self.biomes)
                            if isinstance(item, dict)
                            and item.get("name") == "Plains"
                        )
                    ]
               )
                self.biome_map.append(chosen_biome["name"])
            self.p_world.octaves = chosen_biome["octaves"]
            self.p_world.strengths = chosen_biome["strengths"]
            chunk_data = (height * (1 - chosen_biome["strength"])) + (
                chosen_biome["strength"]
                * self.generate_chunk(
                    self.chunk_size, -
                    chosen_biome["y"][0], chosen_biome["y"][1]
                )
            )
            chunk_data = self.smooth(chunk_data, 20)
            chunk_data = np.full(self.chunk_size, chunk_data[0])
            self.world_height_map = np.concatenate(
                (self.world_height_map, chunk_data), axis=0
            )
        self.world_height_map = self.smooth(self.world_height_map, 8)
        self.world_height_map = self.scale(self.world_height_map, 0, 100)  # Scale to 0-100 range
        self.world_height_map = np.round(self.world_height_map, 0).astype(np.int32) 

    def generate_chunk_map(self, size):
        noise = self.p_biome.generate(size)
        noise = np.round(noise, 0)
        noise = self.scale(noise, -1, 1)
        noise = self.smooth(noise, 64)
        return noise

    def expand_x(self, x, new_length):
        x_min, x_max = np.min(x), np.max(x)
        x_new = np.linspace(x_min, x_max, new_length)
        return x_new

    def scale(self, arr, min=-1, max=1):
        arr_min = np.min(arr)
        arr_max = np.max(arr)
        if arr_min == arr_max:
            return np.full_like(arr, min)
        return np.clip(min + ((arr - arr_min) * (max - min)) / (arr_max - arr_min), min, max)

    def smooth(self, arr, window):
        return np.convolve(arr, np.ones(window) / window, mode="valid")

    def save(self):
        pass

    def __str__(self):
        return f"{self.seed}"


def plot(arr):
    plt.figure(figsize=(12, 6))
    plt.plot(arr)
    plt.title("Merged Simplex Noise with Octaves 1, 3, 16, 24")
    plt.xlabel("Position")
    plt.ylabel("Height")
    plt.show()


# if __name__ == "__main__":
# while True:
# w = World_Generator(2087500335)
# plot(w.world_height_map)
# # plot(w.chunk_biome_map)
# w.generate_world()
# # w.generate_world()
# print(len(w.world_height_map))
# plot(w.world_height_map)
# # plot(w.smooth(w.world,8))


class Tile:
    def __init__(self, x, y, color, size):
        self.x, self.y, self.color, self.size = x, y, color, size
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    def __str__(self):
        return f"x: {self.x}, y: {self.y}, c: {self.color}, size: {self.size}"

class Game(Scene):
    def __init__(self, screen_size):
        super().__init__(screen_size)
        self.world = World_Generator(710080875)
        self.font = pygame.font.SysFont(None, 30)
        self.zoom = 1
        self.block_size = 64 * self.zoom
        self.block_size_org = 64
        self.height = screen_size[1]
        self.width = screen_size[0]

        # Scale the world height map to a reasonable range
        max_height = np.max(self.world.world_height_map)
        min_height = np.min(self.world.world_height_map)
        self.world.world_height_map = (self.world.world_height_map - min_height) / (max_height - min_height) * 100

        # Ensure the player starts at a valid position
        start_height = int(self.world.world_height_map[0])
        self.player = Player(
            8,  # Starting X position
            self.height - (start_height + 1) * self.block_size,  # Starting Y position
            self.block_size
        )
        self.entities.append(self.player)

        self.camera = Camera(self.player, screen_size, zoom=self.zoom)
        
        # Update the platforms creation to use the scaled height map
        self.platforms = [
            [
                Tile(x * self.block_size_org, 
                     self.height - (y + 1) * self.block_size_org, 
                     self.world.blocks[id]["color"], 
                     self.block_size_org) if id != 0 else None
                for x, id in enumerate(row)
            ]
            for y, row in enumerate(self.world.terrain)
        ]
        
        self.visible_platforms = []
        self.last_camera_position = (0, 0, self.zoom)
        self.profiler = cProfile.Profile()
        self.profiling = True

    def get_visible_platforms(self):
        current_camera_position = (self.camera.offset_x, self.camera.offset_y, self.zoom)
        if current_camera_position == self.last_camera_position and self.visible_platforms:
            return self.visible_platforms

        # Calculate visible area in world coordinates
        left = int(self.camera.offset_x // (self.block_size_org * self.zoom))
        top = int(self.camera.offset_y // (self.block_size_org * self.zoom))
        right = left + int(self.width // (self.block_size_org * self.zoom)) + 1
        bottom = top + int(self.height // (self.block_size_org * self.zoom)) + 1

        # Ensure we don't go out of bounds
        left = max(0, left)
        top = max(0, top)
        right = min(len(self.platforms[0]), right)
        bottom = min(len(self.platforms), bottom)

        visible_platforms = [
            tile
            for y in range(top, bottom)
            for tile in self.platforms[y][left:right]
            if tile is not None
        ]

        self.visible_platforms = visible_platforms
        self.last_camera_position = current_camera_position
        return visible_platforms

    def update(self):
        if self.profiling:
            self.profiler.enable()

        super().update()
        self.player.update(self.visible_platforms)  # Only check collision with visible platforms
        self.camera.update()

        if self.profiling:
            self.profiler.disable()

    def toggle_profiling(self):
        self.profiling = not self.profiling
        if not self.profiling:
            s = io.StringIO()
            ps = pstats.Stats(self.profiler, stream=s).sort_stats('cumulative')
            ps.print_stats()
            print(s.getvalue())
            self.profiler.clear()

    def draw(self):
        self.screen.fill((135, 206, 235))  # Light blue background

        # Draw platforms
        visible_platforms = self.get_visible_platforms()
        for platform in visible_platforms:
            screen_x = (platform.x * self.block_size_org - self.camera.offset_x) * self.zoom
            screen_y = (platform.y * self.block_size_org - self.camera.offset_y) * self.zoom
            screen_rect = pygame.Rect(
                screen_x,
                screen_y,
                self.block_size_org * self.zoom,
                self.block_size_org * self.zoom
            )
            pygame.draw.rect(self.screen, platform.color, screen_rect)

        # Draw entities
        for entity in self.entities:
            entity.draw(self.screen, self.camera)

        # Draw FPS and debug info
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(f"FPS: {fps}", True, (255, 0, 0))
        l = str(len(visible_platforms))
        l_text = self.font.render(f"Visible Tiles: {l}", True, (255, 0, 0))

        self.screen.blit(fps_text, (10, 10))
        self.screen.blit(l_text, (10, 40))

        # Draw camera debug rectangle
        # pygame.draw.rect(self.screen, "yellow", self.camera.rect, 2)

    def handle_events(self, event):
        
        if event.type == pygame.MOUSEWHEEL:
            self.zoom = max(0.8, min(self.zoom + event.y * 0.1, 2))
            self.camera.adjust_zoom(event.y * 0.1)
            self.block_size = self.block_size_org * self.zoom
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS:

                self.zoom = max(0.8, min(self.zoom-1 * 0.1, 2))
                self.camera.adjust_zoom(-1 * 0.1)
                self.block_size = self.block_size_org * self.zoom
            elif event.key == pygame.K_PLUS:

                self.zoom = max(0.8, min(self.zoom+1 * 0.1, 2))
                self.camera.adjust_zoom(1 * 0.1)
                self.block_size = self.block_size_org * self.zoom
            elif event.key == pygame.K_p:
                self.toggle_profiling()
    def pre_run(self):
        pass

class Camera:
    def __init__(self, target, screen_size, margins=[100, 200], zoom=1):
        self.target = target
        self.width, self.height = screen_size
        self.margins = margins
        self.zoom = zoom
        self.offset_x = 0
        self.offset_y = 0

    def update(self):
        # Calculate the target's position on screen
        target_screen_x = self.target.rect.centerx * self.zoom - self.offset_x
        target_screen_y = self.target.rect.centery * self.zoom - self.offset_y

        # Adjust offset if target is outside the margins
        if target_screen_x < self.margins[0]:
            self.offset_x += target_screen_x - self.margins[0]
        elif target_screen_x > self.width - self.margins[0]:
            self.offset_x += target_screen_x - (self.width - self.margins[0])

        if target_screen_y < self.margins[1]:
            self.offset_y += target_screen_y - self.margins[1]
        elif target_screen_y > self.height - self.margins[1]:
            self.offset_y += target_screen_y - (self.height - self.margins[1])

    def apply(self, rect):
        return pygame.Rect(
            (rect.x * self.zoom - self.offset_x),
            (rect.y * self.zoom - self.offset_y),
            rect.width * self.zoom,
            rect.height * self.zoom
        )

    def adjust_zoom(self, amount):
        old_zoom = self.zoom
        self.zoom = max(0.8, min(self.zoom + amount, 2))
        zoom_factor = self.zoom / old_zoom
        self.offset_x = self.offset_x * zoom_factor + (1 - zoom_factor) * self.width / 2
        self.offset_y = self.offset_y * zoom_factor + (1 - zoom_factor) * self.height / 2
