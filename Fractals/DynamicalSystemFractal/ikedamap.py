import numpy as np
import matplotlib.pyplot as plt

class IkedaMap:
    def __init__(self, mu=0.9, x0=0.1, y0=0.1, max_iter=1000):
        """
        Initialize the Ikeda Map with parameters.
        
        :param mu: The control parameter for the Ikeda map (default is 0.9).
        :param x0: Initial value for x.
        :param y0: Initial value for y.
        :param max_iter: Number of iterations to run the map.
        """
        self.mu = mu
        self.x0 = x0
        self.y0 = y0
        self.max_iter = max_iter
        self.x_values = []
        self.y_values = []

    def iterate(self):
        """
        Perform the Ikeda map iterations and store the x and y values.
        """
        x, y = self.x0, self.y0
        
        # Iterate the map for `max_iter` iterations
        for _ in range(self.max_iter):
            x_new = 1 - self.mu * (x * np.cos(y) + y * np.sin(x))
            y_new = self.mu * (x * np.sin(y) - y * np.cos(x))
            
            # Store the values for plotting
            self.x_values.append(x_new)
            self.y_values.append(y_new)
            
            # Update x, y for next iteration
            x, y = x_new, y_new

    def plot(self):
        """
        Plot the trajectory of the Ikeda map.
        """
        if not self.x_values or not self.y_values:
            self.iterate()  # Generate the map if not already done
        
        plt.figure(figsize=(8, 8))
        plt.plot(self.x_values, self.y_values, ',k', markersize=0.5)
        plt.title(f"Ikeda Map (mu = {self.mu})")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.axis('equal')
        plt.show()

# Example usage
if __name__ == '__main__':
    ikeda = IkedaMap(mu=0.9, x0=0.1, y0=0.1, max_iter=10000)
    ikeda.iterate()  # Run the iterations
    ikeda.plot()  # Plot the result
