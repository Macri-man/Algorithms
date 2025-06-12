import numpy as np
import matplotlib.pyplot as plt

def custom_cumsum(arr):
    """Custom function to calculate the cumulative sum."""
    cumsum = np.zeros_like(arr)  # Initialize array to store the cumulative sum
    cumsum[0] = arr[0]  # The first element is the same
    for i in range(1, len(arr)):
        cumsum[i] = cumsum[i-1] + arr[i]  # Add each element to the previous cumulative sum
    return cumsum

def brownian_1d(size=1000):
    """Generate 1D Brownian motion using custom cumulative sum."""
    steps = np.random.randn(size)  # Random steps
    return custom_cumsum(steps)  # Use custom cumulative sum function

def plot_brownian_1d(size=2000):
    """Generate and plot 1D Brownian noise."""
    data_1d = brownian_1d(size)
    plt.plot(data_1d)
    plt.title('1D Brownian Noise')
    plt.xlabel('Time')
    plt.ylabel('Position')
    plt.show()

# Call the function to plot 1D Brownian noise
plot_brownian_1d()

def brownian_2d(size=2000):
    """Generate 2D Brownian motion using custom cumulative sum."""
    x = brownian_1d(size)
    y = brownian_1d(size)
    return x, y

def plot_brownian_2d(size=2000):
    """Generate and plot 2D Brownian noise."""
    x, y = brownian_2d(size)
    plt.plot(x, y)
    plt.title('2D Brownian Noise')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

# Call the function to plot 2D Brownian noise
plot_brownian_2d()

def generate_grayscale_image(x, y, grid_size=(500, 500)):
    """Generate a grayscale image from 2D Brownian motion."""
    # Create an empty grid (image) with the specified size
    image = np.zeros(grid_size)

    # Normalize the Brownian motion coordinates to fit the image size
    x_normalized = np.interp(x, (x.min(), x.max()), (0, grid_size[0] - 1))
    y_normalized = np.interp(y, (y.min(), y.max()), (0, grid_size[1] - 1))

    # Convert normalized values to integers for pixel positions
    x_scaled = np.int32(x_normalized)
    y_scaled = np.int32(y_normalized)

    # Increase the pixel value at each (x, y) position
    for i in range(len(x)):
        image[y_scaled[i], x_scaled[i]] += 1

    # Normalize the image to be in the range [0, 255]
    image = np.clip(image / image.max() * 255, 0, 255).astype(np.uint8)

    return image

def plot_grayscale_image(image):
    """Plot the generated grayscale image."""
    plt.imshow(image, cmap='gray', origin='upper')
    plt.title("Grayscale Image of 2D Brownian Motion")
    plt.axis('off')
    plt.show()

# Generate 2D Brownian motion
x, y = brownian_2d()

# Generate a grayscale image from the Brownian motion
image = generate_grayscale_image(x, y, grid_size=(500, 500))

# Plot the resulting image
plot_grayscale_image(image)

def brownian_3d(size=2000):
    """Generate 3D Brownian motion using custom cumulative sum."""
    x = brownian_1d(size)
    y = brownian_1d(size)
    z = brownian_1d(size)
    return x, y, z

def plot_brownian_3d(size=2000):
    """Generate and plot 3D Brownian noise."""
    x, y, z = brownian_3d(size)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z)
    ax.set_title('3D Brownian Noise')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

# Call the function to plot 3D Brownian noise
plot_brownian_3d()


