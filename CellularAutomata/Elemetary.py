import numpy as np
import matplotlib.pyplot as plt

def apply_rule(rule_number, current_state):
    rule_bin = np.array([int(x) for x in np.binary_repr(rule_number, width=8)])
    next_state = np.zeros_like(current_state)
    
    for i in range(1, len(current_state) - 1):
        neighborhood = (current_state[i-1], current_state[i], current_state[i+1])
        index = 7 - (neighborhood[0] * 4 + neighborhood[1] * 2 + neighborhood[2])
        next_state[i] = rule_bin[index]
    return next_state

def plot_automaton(rule_number, grid_size=200, generations=100):
    # Initialize the grid
    grid = np.zeros((generations, grid_size), dtype=int)
    grid[0, grid_size // 2] = 1  # Set the initial condition (a single live cell in the center)

    # Evolve the grid
    for i in range(1, generations):
        grid[i] = apply_rule(rule_number, grid[i - 1])

    # Plot the results
    plt.imshow(grid, cmap='binary', interpolation='nearest')
    plt.title(f'Elementary Cellular Automaton - Rule {rule_number}')
    plt.xlabel('Cell Position')
    plt.ylabel('Generation')
    plt.show()

plot_automaton(rule_number=30)