import numpy as np
import matplotlib.pyplot as plt
import noise  # Make sure to install the noise library: pip install noise

class OctaveNoise:
    """
    Class to generate octave noise, which is a sum of multiple layers of Perlin noise.
    
    Attributes:
    octaves (int): The number of octaves (layers of noise).
    persistence (float): Controls how much the amplitude of each octave decreases.
    lacunarity (float): Controls how much the frequency of each octave increases.
    """
    
    def __init__(self, octaves, persistence, lacunarity):
        """
        Initializes the OctaveNoise object with given parameters.
        
        Parameters:
        octaves (int): Number of octaves for the noise generation.
        persistence (float): Persistence value that affects the amplitude reduction.
        lacunarity (float): Lacunarity value that affects the frequency increase.
        """
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity

    def generate_noise(self, x, y):
        """
        Generates the octave noise value at a given coordinate (x, y).
        
        Parameters:
        x (float): The x-coordinate.
        y (float): The y-coordinate.
        
        Returns:
        float: The normalized noise value at (x, y).
        """
        total = 0.0
        frequency = 1.0
        amplitude = 1.0

        # Sum the contributions from each octave
        for _ in range(self.octaves):
            total += amplitude * noise.pnoise2(x * frequency, y * frequency, 
                                               repeatx=1024, repeaty=1024, base=0)
            frequency *= self.lacunarity  # Increase frequency for higher octaves
            amplitude *= self.persistence  # Decrease amplitude for higher octaves

        # Normalize the output to the range [0, 1]
        max_value = sum(self.persistence ** i for i in range(self.octaves))
        return total / max_value


def generate_noise_grid(grid_size, octave_noise, scale=0.1):
    """
    Generates a grid of octave noise values.
    
    Parameters:
    grid_size (int): The size of the grid (grid_size x grid_size).
    octave_noise (OctaveNoise): The OctaveNoise object used to generate noise.
    scale (float): The scaling factor applied to the coordinates to control noise "zoom".
    
    Returns:
    np.ndarray: A 2D array of noise values.
    """
    noise_values = np.zeros((grid_size, grid_size))
    
    for x in range(grid_size):
        for y in range(grid_size):
            noise_values[x, y] = octave_noise.generate_noise(x * scale, y * scale)

    return noise_values


def visualize_noise(noise_values):
    """
    Visualizes the generated noise values as an image.
    
    Parameters:
    noise_values (np.ndarray): A 2D array of noise values.
    """
    plt.imshow(noise_values, cmap='gray')
    plt.colorbar()
    plt.title("Octave Noise")
    plt.show()


# Example usage
if __name__ == "__main__":
    # Parameters for noise generation
    grid_size = 256  # Size of the noise grid
    octaves = 6  # Number of octaves
    persistence = 0.5  # Persistence value
    lacunarity = 2.0  # Lacunarity value

    # Create an OctaveNoise instance
    octave_noise = OctaveNoise(octaves, persistence, lacunarity)

    # Generate the noise grid
    noise_values = generate_noise_grid(grid_size, octave_noise)

    # Visualize the noise
    visualize_noise(noise_values)
