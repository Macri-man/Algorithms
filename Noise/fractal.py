import numpy as np
import matplotlib.pyplot as plt
import noise  # Make sure to install the noise library: pip install noise

def generate_fractal_noise(x, y, octaves, persistence, lacunarity):
    """
    Generate fractal noise at coordinates (x, y) using multiple octaves.

    :param x: The x-coordinate.
    :param y: The y-coordinate.
    :param octaves: Number of noise layers.
    :param persistence: Controls how much the amplitude decreases with each octave.
    :param lacunarity: Controls how much the frequency increases with each octave.
    :return: The fractal noise value at the given coordinates.
    """
    total = 0.0
    frequency = 1.0
    amplitude = 1.0

    for _ in range(octaves):
        total += amplitude * noise.pnoise2(x * frequency, y * frequency, repeatx=1024, repeaty=1024, base=0)
        frequency *= lacunarity  # Increase frequency
        amplitude *= persistence  # Decrease amplitude

    return total

def generate_noise_grid(grid_size, octaves, persistence, lacunarity, scale=0.1):
    """
    Generate a 2D array of fractal noise values.

    :param grid_size: The size of the grid (e.g., 256x256).
    :param octaves: Number of noise layers.
    :param persistence: Controls how much the amplitude decreases with each octave.
    :param lacunarity: Controls how much the frequency increases with each octave.
    :param scale: A scaling factor to adjust the noise resolution.
    :return: A 2D numpy array of noise values.
    """
    noise_values = np.zeros((grid_size, grid_size))

    for x in range(grid_size):
        for y in range(grid_size):
            noise_values[x, y] = generate_fractal_noise(x * scale, y * scale, octaves, persistence, lacunarity)

    return noise_values

def visualize_noise(noise_values):
    """
    Visualize the generated fractal noise using matplotlib.

    :param noise_values: A 2D numpy array containing the noise values.
    """
    plt.imshow(noise_values, cmap='gray')
    plt.colorbar()
    plt.title("Fractal Noise")
    plt.show()

def main():
    """
    Main function to initialize parameters, generate noise, and visualize it.
    """
    # Parameters
    grid_size = 256
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0
    scale = 0.1  # Adjust scale for visual effect

    # Generate fractal noise
    noise_values = generate_noise_grid(grid_size, octaves, persistence, lacunarity, scale)

    # Visualize the generated noise
    visualize_noise(noise_values)

# Run the main function
if __name__ == "__main__":
    main()
