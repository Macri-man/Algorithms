import numpy as np
import matplotlib.pyplot as plt

# Gradient vectors for 2D Simplex Noise (2D vectors)
grad2 = np.array([[1, 1], [-1, 1], [1, -1], [-1, -1],
                  [1, 0], [-1, 0], [0, 1], [0, -1]])

# Permutation table for hashing
p = np.arange(256, dtype=int)  # Use built-in int instead of np.int
np.random.shuffle(p)
perm = np.stack((p, p)).flatten()  # Duplicate the permutation table

def noise(x, y):
    """Generate 2D Simplex noise at the given coordinates (x, y)."""
    # Skewing factor for 2D
    F2 = 0.5 * (np.sqrt(3.0) - 1.0)
    s = (x + y) * 0.5 * (np.sqrt(3.0) - 1.0)  # Skew the coordinates
    i = int(np.floor(x + s))
    j = int(np.floor(y + s))

    # Unskewing factor
    G2 = (3.0 - np.sqrt(3.0)) / 6.0
    x0 = x - (i - (i + j) * G2)  # Unskew the coordinates
    y0 = y - (j - (i + j) * G2)

    # Determine the corner offsets based on x0 and y0
    i1 = 0 if x0 > y0 else 1  # Offset for the second corner
    j1 = 1 - i1  # Offset for the third corner

    # Hash the coordinates for the gradients
    ii = i & 255
    jj = j & 255
    gi0 = perm[ii + perm[jj]] % 8  # Use grad2, so mod 8
    gi1 = perm[ii + i1 + perm[jj + j1]] % 8
    gi2 = perm[ii + 1 + perm[jj + 1]] % 8

    # Compute the contributions from each corner
    t0 = 0.5 - x0 * x0 - y0 * y0
    n0 = 0 if t0 < 0 else (t0 ** 4) * np.dot(grad2[gi0], [x0, y0])
    
    t1 = 0.5 - (x0 - i1 + G2) ** 2 - (y0 - j1 + G2) ** 2
    n1 = 0 if t1 < 0 else (t1 ** 4) * np.dot(grad2[gi1], [x0 - i1 + G2, y0 - j1 + G2])
    
    t2 = 0.5 - (x0 - 1 + 2 * G2) ** 2 - (y0 - 1 + 2 * G2) ** 2
    n2 = 0 if t2 < 0 else (t2 ** 4) * np.dot(grad2[gi2], [x0 - 1 + 2 * G2, y0 - 1 + 2 * G2])

    # Scale the result and return the final value
    return (n0 + n1 + n2) * 70  # Scale factor for better visualization


def generate_noise(width, height, scale=0.1):
    """Generate a 2D noise map."""
    noise_map = np.zeros((width, height))

    for x in range(width):
        for y in range(height):
            noise_map[x][y] = noise(x * scale, y * scale)  # Scale for visual effect

    return noise_map


# Example usage
width, height = 256, 256
noise_map = generate_noise(width, height)

# Visualization of the generated noise
plt.imshow(noise_map, cmap='gray')
plt.colorbar()
plt.title("2D Simplex Noise")
plt.show()
