import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label
from concurrent.futures import ThreadPoolExecutor

# Function to generate a percolation grid with open sites at probability p
def percolation(grid_size, p):
    """
    Create a grid where each site is open with probability p.
    :param grid_size: Size of the grid (grid_size x grid_size)
    :param p: Probability of a site being open (0 <= p <= 1)
    :return: 2D numpy array representing the grid
    """
    return np.random.rand(grid_size, grid_size) < p

# Function to check if percolation occurs
def percolates(grid):
    """
    Check if percolation occurs by determining if the top row
    is connected to the bottom row.
    :param grid: 2D numpy array representing the grid of open/closed sites
    :return: True if percolation occurs, False otherwise
    """
    structure = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    labeled_grid, _ = label(grid, structure)
    top_labels = set(labeled_grid[0, :])
    bottom_labels = set(labeled_grid[-1, :])
    return not top_labels.isdisjoint(bottom_labels)

# Parallelized percolation simulation
def simulate_percolation(grid_size, probabilities):
    """
    Simulate percolation for a range of probabilities using parallel processing.
    :param grid_size: Size of the grid (grid_size x grid_size)
    :param probabilities: List of probabilities to test
    :return: List of percolation results (True/False) for each probability
    """
    with ThreadPoolExecutor() as executor:
        # Map probabilities to results using parallel execution
        results = list(executor.map(lambda p: percolates(percolation(grid_size, p)), probabilities))
    return results

# Function to plot percolation results
def plot_results(probabilities, results):
    """
    Plot the results of the percolation simulation.
    :param probabilities: List of probabilities tested
    :param results: List of percolation results (True/False)
    """
    plt.plot(probabilities, results)
    plt.xlabel('Probability (p)')
    plt.ylabel('Percolation')
    plt.title('Percolation Threshold Estimation')
    plt.grid(True)
    plt.show()

# Main function to run the simulation and plot the results
def main():
    grid_size = 50  # Size of the grid
    probabilities = np.linspace(0.3, 0.7, 100)  # Range of probabilities to test

    # Simulate percolation and get the results
    results = simulate_percolation(grid_size, probabilities)

    # Plot the results
    plot_results(probabilities, results)

# Run the main function
if __name__ == '__main__':
    main()
