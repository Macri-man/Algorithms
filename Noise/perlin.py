import numpy as np
import matplotlib.pyplot as plt

# ---- Perlin Noise Helper Functions ----

def fade(t):
    """Fade function as defined by Ken Perlin. This eases coordinate values."""
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(a, b, t):
    """Linear interpolation between a and b."""
    return a + t * (b - a)

def grad(hash, x, y):
    """Convert low 4 bits of hash code into 8 gradient directions."""
    h = hash & 3  # Convert low 2 bits of hash code
    u = x if h < 2 else y  # Gradient direction
    v = y if h < 2 else x  # Gradient direction
    return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)

def generate_perlin_noise(size):
    """Generate a 2D Perlin noise grid."""
    # Generate random permutation array and duplicate it for wrapping
    permutation = np.random.permutation(256)
    permutation = np.tile(permutation, 2)  # Duplicate for wrapping

    def noise(x, y):
        """Generate Perlin noise at coordinates (x, y)."""
        xi = int(x) & 255  # Wrap the x-coordinate
        yi = int(y) & 255  # Wrap the y-coordinate

        xf = x - int(x)  # Fractional part of x
        yf = y - int(y)  # Fractional part of y

        # Compute fade curves for x and y
        u = fade(xf)
        v = fade(yf)

        # Hash coordinates of the square corners
        aa = permutation[permutation[xi] + yi]
        ab = permutation[permutation[xi] + yi + 1]
        ba = permutation[permutation[xi + 1] + yi]
        bb = permutation[permutation[xi + 1] + yi + 1]

        # Interpolate results from the corners of the square
        x1 = lerp(grad(aa, xf, yf), grad(ba, xf - 1, yf), u)
        x2 = lerp(grad(ab, xf, yf - 1), grad(bb, xf - 1, yf - 1), u)

        # Return final interpolated value (normalized to [0, 1])
        return (lerp(x1, x2, v) + 1) / 2

    return noise

# ---- Example Usage ----

# Generate Perlin noise function with a grid size of 256
perlin_noise = generate_perlin_noise(size=256)

# Create a 2D array to hold noise values
noise_values = np.zeros((256, 256))

# Generate Perlin noise for a scaled grid
for x in range(256):
    for y in range(256):
        noise_values[x][y] = perlin_noise(x * 0.1, y * 0.1)  # Scale for visual effect

# ---- Visualization ----

# Display the generated Perlin noise as a grayscale image
plt.imshow(noise_values, cmap='gray')
plt.colorbar()  # Add a color bar for reference
plt.title("Perlin Noise Visualization")
plt.show()
