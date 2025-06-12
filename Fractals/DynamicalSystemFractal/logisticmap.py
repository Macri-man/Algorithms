import numpy as np
import matplotlib.pyplot as plt

class LogisticMap:
    def __init__(self, r=3.5, x0=0.5, num_iterations=1000):
        """
        Initialize the Logistic Map with the given parameters.
        
        :param r: Growth rate parameter (default is 3.5).
        :param x0: Initial population value (default is 0.5).
        :param num_iterations: Number of iterations to run (default is 1000).
        """
        self.r = r
        self.x0 = x0
        self.num_iterations = num_iterations
        self.values = None

    def iterate(self):
        """
        Iterate the logistic map and store the results.
        """
        x = self.x0
        self.values = np.zeros(self.num_iterations)
        for i in range(self.num_iterations):
            x = self.r * x * (1 - x)
            self.values[i] = x

    def plot(self):
        """
        Plot the logistic map iterations.
        """
        if self.values is None:
            self.iterate()  # Run the logistic map iterations if not already done
            
        plt.figure(figsize=(10, 6))
        plt.plot(self.values, color='b', lw=0.8)
        plt.title(f"Logistic Map: r={self.r}")
        plt.xlabel("Iteration")
        plt.ylabel("Population (x)")
        plt.grid(True)
        plt.show()

    def bifurcation(self, r_min=2.5, r_max=4.0, num_points=1000, num_iterations=1000, last_iterations=100):
        """
        Plot the bifurcation diagram for the logistic map.
        
        :param r_min: Minimum value for r (default is 2.5).
        :param r_max: Maximum value for r (default is 4.0).
        :param num_points: Number of r values to check (default is 1000).
        :param num_iterations: Total number of iterations for each r (default is 1000).
        :param last_iterations: Number of iterations to display in the bifurcation diagram (default is 100).
        """
        r_values = np.linspace(r_min, r_max, num_points)
        x_values = np.zeros(num_points)
        
        plt.figure(figsize=(10, 6))
        for i, r in enumerate(r_values):
            x = 0.5  # Initial condition for each r
            # Iterate and discard first few iterations to allow for transients
            for _ in range(num_iterations - last_iterations):
                x = r * x * (1 - x)
            
            # Plot the last few iterations for the bifurcation diagram
            for _ in range(last_iterations):
                x = r * x * (1 - x)
                plt.plot([r], [x], ',k', alpha=0.25)  # ',' makes small points
        
        plt.title("Bifurcation Diagram for Logistic Map")
        plt.xlabel("Growth Rate (r)")
        plt.ylabel("Population (x)")
        plt.show()

# Example usage
if __name__ == '__main__':
    # Logistic Map iteration plot
    logistic_map = LogisticMap(r=3.5, x0=0.5, num_iterations=1000)
    logistic_map.iterate()  # Run the logistic map iterations
    logistic_map.plot()  # Plot the iterations

    # Bifurcation diagram
    logistic_map.bifurcation(r_min=2.5, r_max=4.0, num_points=1000, num_iterations=1000, last_iterations=100)
