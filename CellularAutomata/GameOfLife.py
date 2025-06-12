import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def initialize_grid(grid_size, alive_probability=0.2):
    return np.random.choice([0, 1], size=(grid_size, grid_size), p=[1 - alive_probability, alive_probability])

def count_neighbors(grid, x, y):
    total = int(
        (grid[x, (y-1)%grid.shape[1]] + grid[x, (y+1)%grid.shape[1]] +
         grid[(x-1)%grid.shape[0], y] + grid[(x+1)%grid.shape[0], y] +
         grid[(x-1)%grid.shape[0], (y-1)%grid.shape[1]] + grid[(x-1)%grid.shape[0], (y+1)%grid.shape[1]] +
         grid[(x+1)%grid.shape[0], (y-1)%grid.shape[1]] + grid[(x+1)%grid.shape[0], (y+1)%grid.shape[1]]))
    return total

def apply_rules(grid, x, y, total):
    if grid[x, y] == 1:  # Live cell
        if total < 2 or total > 3:
            return 0  # Dies
        return 1  # Stays alive
    else:  # Dead cell
        if total == 3:
            return 1  # Becomes alive
    return 0  # Stays dead

def update(frame, grid, img):
    new_grid = grid.copy()
    
    # Update each cell based on its neighbors
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            total = count_neighbors(grid, x, y)
            new_grid[x, y] = apply_rules(grid, x, y, total)

    grid[:] = new_grid  # Update the grid with the new state
    img.set_array(grid)  # Update the displayed image
    return img,

def create_animation(grid_size=50, frames=200, interval=100, save_path="game_of_life.mp4"):
    # Initialize grid
    grid = initialize_grid(grid_size)

    # Set up the figure for animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, cmap='binary')

    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=frames, interval=interval, fargs=(grid, img), blit=True)

    # Save the animation as a video file (MP4)
    ani.save(save_path, writer='ffmpeg', fps=12)

    plt.show()

# Call the function to create and save the animation
create_animation(save_path="game_of_life.mp4")
