import noise  # Import the Simplex noise function from the noise library
import numpy as np
import matplotlib.pyplot as plt
import random


def generate_noise(size, octaves, strength):
    x = np.zeros((len(octaves), size))

    for j, (octave, s) in enumerate(zip(octaves, strength)):
        l = random.randint(0, 500)
        print(l)
        for i in range(size):
            x[j, i] = noise.pnoise1(
                i / 100.0, octaves=octave, persistence=s, base=l
            )

    # Combine all octaves into a 1D array
    return x.sum(axis=0)


def scale(arr, min=-1, max=1):
    arr_min = np.min(arr)
    arr_max = np.max(arr)
    return min + ((arr - arr_min) * (max - min)) / (arr_max - arr_min)


def smooth(arr, window):
    return np.convolve(arr, np.ones(window) / window, mode="valid")


def generate_chunk_biomes(seed=689, no_of_chunks=1000):
    # Set the seed value
    np.random.seed(seed)
    random.seed(seed)
    # Generate noise
    noise = generate_noise(no_of_chunks, [1, 3, 24], [0.5, 0.3, 0.2])
    noise = np.round(noise, 0)
    noise = scale(noise, -1, 1)
    noise = smooth(noise, 16)
    return noise


def plot(arr):
    plt.figure(figsize=(12, 6))
    plt.plot(arr)
    plt.title("Merged Simplex Noise with Octaves 1, 3, 16, 24")
    plt.xlabel("Position")
    plt.ylabel("Height")
    plt.show()


if __name__ == "__main__":
    plot(generate_chunk_biomes(no_of_chunks=10000))
