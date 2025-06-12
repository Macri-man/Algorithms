import numpy as np
import matplotlib.pyplot as plt

def generate_points(grid_size, num_points):
    """Generate random feature points within the grid."""
    return np.random.rand(num_points, 2) * grid_size

def distance(p1, p2):
    """Calculate squared distance to avoid computing square root."""
    return np.sum((p1 - p2) ** 2)

def noise(x, y, points):
    """Generate Worley noise at coordinates (x, y)."""
    nearest_distances = []

    # Check distances to all feature points
    for point in points:
        dist = distance(point, np.array([x, y]))
        nearest_distances.append(dist)

    # Sort distances to find the nearest points
    nearest_distances.sort()

    # Use the distance to the closest feature point
    return np.sqrt(nearest_distances[0])  # Return the distance as noise value

# Example usage
grid_size = 256
num_points = 50
points = generate_points(grid_size, num_points)
noise_values = np.zeros((grid_size, grid_size))

for x in range(grid_size):
    for y in range(grid_size):
        noise_values[x, y] = noise(x, y, points)

# Visualization
plt.imshow(noise_values, cmap='gray')
plt.colorbar()
plt.title("Worley Noise")
plt.show()
