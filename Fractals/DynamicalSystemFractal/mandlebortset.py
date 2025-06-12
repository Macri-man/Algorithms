import numpy as np
import matplotlib.pyplot as plt

class MandelbrotSet:
    def __init__(self, x_min=-2.0, x_max=1.0, y_min=-1.5, y_max=1.5, width=800, height=800, max_iter=256):
        """
        Initialize the Mandelbrot Set generator.
        
        :param x_min: Minimum x value (real part of complex numbers).
        :param x_max: Maximum x value (real part of complex numbers).
        :param y_min: Minimum y value (imaginary part of complex numbers).
        :param y_max: Maximum y value (imaginary part of complex numbers).
        :param width: Width of the generated image.
        :param height: Height of the generated image.
        :param max_iter: Maximum number of iterations before considering a point to have "escaped".
        """
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.width = width
        self.height = height
        self.max_iter = max_iter
        self.img = None

    def generate(self):
        """
        Generate the Mandelbrot set and store the result in the `img` attribute.
        """
        # Create a grid of complex numbers
        x = np.linspace(self.x_min, self.x_max, self.width)
        y = np.linspace(self.y_min, self.y_max, self.height)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y  # Complex grid
        
        # Initialize an array to store the iteration counts
        self.img = np.zeros(Z.shape, dtype=int)
        
        # Iterate over each point in the grid
        for i in range(self.max_iter):
            mask = np.abs(Z) <= 2  # Only iterate for points that haven't escaped
            Z[mask] = Z[mask]**2 + (X + 1j * Y)[mask]  # Mandelbrot equation: Z = Z^2 + c
            self.img += mask  # Increment the count for each point that hasn't escaped yet

    def plot(self):
        """
        Plot the Mandelbrot set using matplotlib.
        """
        if self.img is None:
            self.generate()  # Generate the image if not already done
        plt.figure(figsize=(8, 8))
        plt.imshow(self.img, extent=(self.x_min, self.x_max, self.y_min, self.y_max), cmap='inferno', origin='lower')
        plt.title("Mandelbrot Set")
        plt.colorbar()
        plt.show()

# Example usage
if __name__ == '__main__':
    mandelbrot = MandelbrotSet(x_min=-2.0, x_max=1.0, y_min=-1.5, y_max=1.5, width=800, height=800, max_iter=256)
    mandelbrot.generate()  # Generate the Mandelbrot set
    mandelbrot.plot()  # Plot the Mandelbrot set
