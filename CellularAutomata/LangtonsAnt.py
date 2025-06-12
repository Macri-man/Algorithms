import numpy as np
import matplotlib.pyplot as plt

# Directions: 0 = Up, 1 = Right, 2 = Down, 3 = Left
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def initialize_grid(grid_size):
    # Initialize the grid with black cells (0)
    return np.zeros((grid_size, grid_size), dtype=int)

def step(grid, ant_position, ant_direction):
    x, y = ant_position

    # Check the color of the current cell
    if grid[x, y] == 0:  # If the cell is black (0)
        # Turn the ant 90 degrees clockwise (right)
        ant_direction = (ant_direction + 1) % 4
        grid[x, y] = 1  # Flip the cell to white (1)
    else:  # If the cell is white (1)
        # Turn the ant 90 degrees counterclockwise (left)
        ant_direction = (ant_direction - 1) % 4
        grid[x, y] = 0  # Flip the cell to black (0)

    # Move the ant one step forward in the direction it is facing
    dx, dy = directions[ant_direction]
    ant_position = (x + dx, y + dy)

    return grid, ant_position, ant_direction

def run_simulation(grid_size, steps):
    # Initialize the grid and set the ant's initial position and direction
    grid = initialize_grid(grid_size)
    ant_position = (grid_size // 2, grid_size // 2)  # Ant starts at the center of the grid
    ant_direction = 0  # Initial direction: 0 = Up

    # Run the simulation for the specified number of steps
    for _ in range(steps):
        grid, ant_position, ant_direction = step(grid, ant_position, ant_direction)
    return grid

def visualize(grid):
    # Visualize the final grid using matplotlib
    plt.imshow(grid, cmap='binary', interpolation='nearest')
    plt.show()

# Set grid size and number of steps
grid_size = 100
steps = 11000

# Run the simulation
final_grid = run_simulation(grid_size, steps)

# Visualize the final grid
visualize(final_grid)
