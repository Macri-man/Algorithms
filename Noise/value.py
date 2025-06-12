import numpy as np
import matplotlib.pyplot as plt

def interpolate(x, a, b):
    """Linear interpolation between a and b based on x."""
    return a + (b - a) * x

def smoothstep(t):
    """Smoothstep function to create smoother transitions."""
    return t * t * (3 - 2 * t)

def generate_value_noise(grid_size, scale):
    """Generate value noise with the given grid size and scale."""
    values = np.random.rand(grid_size, grid_size)  # Random values at grid points
    
    def noise(x, y):
        """Generate value noise at coordinates (x, y)."""
        # Determine grid cell
        x0 = int(x) % grid_size
        y0 = int(y) % grid_size
        x1 = (x0 + 1) % grid_size
        y1 = (y0 + 1) % grid_size

        # Relative coordinates
        sx = x - int(x)
        sy = y - int(y)

        # Smoothstep interpolation
        sx = smoothstep(sx)
        sy = smoothstep(sy)

        # Interpolate between the four grid points
        top = interpolate(sx, values[x0, y0], values[x1, y0])
        bottom = interpolate(sx, values[x0, y1], values[x1, y1])
        
        return interpolate(sy, top, bottom)
    
    return noise

# Example usage
grid_size = 256
scale = 0.1
value_noise = generate_value_noise(grid_size, scale)
noise_values = np.zeros((grid_size, grid_size))

for x in range(grid_size):
    for y in range(grid_size):
        noise_values[x, y] = value_noise(x * scale, y * scale)

# Visualization
plt.imshow(noise_values, cmap='gray')
plt.colorbar()
plt.title("Value Noise")
plt.show()
