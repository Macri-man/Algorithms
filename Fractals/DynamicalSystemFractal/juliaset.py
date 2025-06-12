import numpy as np
import matplotlib.pyplot as plt

class JuliaSet:
    def __init__(self, c, x_min=-2, x_max=2, y_min=-2, y_max=2, width=800, height=800, max_iter=256):
        """
        Initialize the Julia Set fractal generator.

        :param c: Complex constant 'c' used in the iteration (c = a + bi).
        :param x_min: Minimum x value (real part of complex numbers).
        :param x_max: Maximum x value (real part of complex numbers).
        :param y_min: Minimum y value (imaginary part of complex numbers).
        :param y_max: Maximum y value (imaginary part of complex numbers).
        :param width: Width of the generated image.
        :param height: Height of the generated image.
        :param max_iter: Maximum number of iterations to test for escape.
        """
        self.c = c
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
        Generate the Julia Set fractal and store the result in the `img` attribute.
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
            mask = np.abs(Z) <= 1000  # Only iterate for points that haven't escaped
            Z[mask] = Z[mask]**2 + self.c  # Julia map iteration: Z = Z^2 + c
            self.img += mask  # Increment the count for each point that hasn't escaped yet

    def plot(self):
        """
        Plot the Julia Set fractal using matplotlib.
        """
        if self.img is None:
            self.generate()  # Generate the image if not already done
        plt.figure(figsize=(8, 8))
        plt.imshow(self.img, extent=(self.x_min, self.x_max, self.y_min, self.y_max), cmap='inferno', origin='lower')
        plt.title(f"Julia Set (c = {self.c})")
        plt.colorbar()
        plt.show()

# Example usage
if __name__ == '__main__':
    # Create a Julia set instance with a specific value for c
    c = -0.7 + 0.27015j  # A typical value for c in the Julia set
    julia = JuliaSet(c)
    julia.generate()  # Generate the Julia set
    julia.plot()  # Plot the Julia set
