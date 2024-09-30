import numpy as np
from noise import pnoise2
import multiprocessing
import ctypes
import cProfile


def generate_block_ids_batch(x_start, x_end, y_max_values, world_height, world_width, shared_array_base):
    """
    Generate blocks for a batch of columns based on the height map using shared memory.
    Each process works on a range of x-coordinates.
    """
    # Convert the shared array to a numpy array
    shared_array = np.ctypeslib.as_array(shared_array_base.get_obj())
    shared_array = shared_array.reshape(world_height, world_width)
    print(x_start)

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
    noise_value = pnoise2(x * scale, y * scale, octaves=octaves, persistence=persistence,
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


def main():
    world_height = 250
    world_width = 32000

    # Generate a height map with random heights
    world_height_map = np.random.randint(
        low=0, high=50, size=world_width, dtype=np.uint8)

    # Generate the world using multiprocessing
    world = generate_world(world_width, world_height, world_height_map)

    # Print a portion of the world for verification
    print(world[:20, :40])


# Run the main function with profiling enabled
if __name__ == '__main__':
    cProfile.run('main()', sort='ncalls')
