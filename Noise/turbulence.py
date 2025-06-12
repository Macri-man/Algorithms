import numpy as np
import matplotlib.pyplot as plt
import noise

def generate_turbulence_noise(x, y, octaves, persistence, lacunarity):
    """
    Generate turbulence noise using multiple octaves.

    Parameters:
        x (numpy.ndarray): x-coordinates for the noise.
        y (numpy.ndarray): y-coordinates for the noise.
        octaves (int): Number of noise layers (octaves).
        persistence (float): Amplitude scaling factor between octaves.
        lacunarity (float): Frequency scaling factor between octaves.

    Returns:
        numpy.ndarray: 2D array of turbulence noise values.
    """
    total = np.zeros_like(x)
    frequency = 1.0
    amplitude = 1.0
    
    # Generate noise over multiple octaves
    for _ in range(octaves):
        total += amplitude * np.vectorize(lambda x, y: noise.pnoise2(x, y, repeatx=1024, repeaty=1024, base=0))(x * frequency, y * frequency)
        frequency *= lacunarity  # Increase frequency
        amplitude *= persistence  # Decrease amplitude
    
    return np.abs(total)  # Use absolute value to enhance turbulence effect

def generate_grid(grid_size):
    """
    Generate a mesh grid for the x and y coordinates.

    Parameters:
        grid_size (int): The size of the grid (height and width).

    Returns:
        tuple: meshgrid of x and y coordinates.
    """
    x = np.arange(grid_size)
    y = np.arange(grid_size)
    return np.meshgrid(x, y)

def plot_turbulence(turbulence_values):
    """
    Plot the generated turbulence noise as an image.

    Parameters:
        turbulence_values (numpy.ndarray): The 2D array of turbulence values to visualize.
    """
    plt.imshow(turbulence_values, cmap='gray')
    plt.colorbar()
    plt.title("Turbulence Noise")
    plt.axis('off')
    plt.show()

def main():
    """
    Main function to generate and visualize turbulence noise.
    """
    # Configuration parameters
    grid_size = 256
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0
    
    # Generate grid coordinates
    x, y = generate_grid(grid_size)
    
    # Generate turbulence noise values
    turbulence_values = generate_turbulence_noise(x * 0.1, y * 0.1, octaves, persistence, lacunarity)
    
    # Plot the resulting turbulence noise
    plot_turbulence(turbulence_values)

if __name__ == "__main__":
    main()
