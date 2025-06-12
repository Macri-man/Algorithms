import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import numpy as np

class CustomLayoutAnimator:
    def __init__(self, layout_config, figsize=(10, 6)):
        """
        Create a figure using a custom layout.
        
        layout_config: dict with keys:
           "grid": tuple (nrows, ncols)
           "subplots": list of subplot specifications. Each specification is a dict with:
                "pos": (row_slice, col_slice) where row_slice and col_slice can be slice or int.
                "title": (optional) title for the axis.
        Example:
           layout_config = {
               "grid": (2, 2),
               "subplots": [
                   {"pos": (slice(0, 2), slice(0, 1)), "title": "Predator/Prey"}, 
                   {"pos": (slice(0, 1), slice(1, 2)), "title": "Food Field"},
                   {"pos": (slice(1, 2), slice(1, 2)), "title": "Population"}
               ]
           }
        """
        self.fig = plt.figure(figsize=figsize)
        nrows, ncols = layout_config.get("grid", (1, 1))
        gs = gridspec.GridSpec(nrows, ncols)
        
        self.axes = []
        for ax_spec in layout_config.get("subplots", []):
            row_pos, col_pos = ax_spec["pos"]
            ax = self.fig.add_subplot(gs[row_pos, col_pos])
            if "title" in ax_spec:
                ax.set_title(ax_spec["title"])
            self.axes.append(ax)
            
        self.anim = None

    def set_animator(self, init_func, update_func, interval=100, frames=None):
        """
        Set a single animator that will update all subplots at once.
        
        Both init_func and update_func must return a tuple of Matplotlib artists
        that will be redrawn (for blitting).
        """
        self.anim = animation.FuncAnimation(
            self.fig,
            update_func,
            init_func=init_func,
            interval=interval,
            frames=frames,
            blit=True,
            cache_frame_data=False
        )

    def show(self):
        plt.tight_layout()
        plt.show()


# ---------------------
# Example usage with custom layout
# ---------------------

def simulation_example():
    # Define custom layout:
    # Left: one subplot (spanning all rows in first column)
    # Right: two subplots stacked vertically in second column.
    layout_config = {
        "grid": (2, 2),  # overall grid has 2 rows and 2 columns
        "subplots": [
            {"pos": (slice(0, 2), 0), "title": "Predator/Prey"},     # left subplot spans both rows in col 0
            {"pos": (0, 1), "title": "Food Field"},                  # top right subplot at grid position (0,1)
            {"pos": (1, 1), "title": "Population"}                   # bottom right subplot at grid position (1,1)
        ]
    }
    
    animator = CustomLayoutAnimator(layout_config, figsize=(12, 6))
    
    # ---------- Simulation Data ----------
    # Left subplot (Predator/Prey)
    num_entities = 20
    pos = np.random.rand(num_entities, 2)
    vel = (np.random.rand(num_entities, 2) - 0.5) * 0.05
    scatter = None

    # Top right subplot (Food Field)
    x, y = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))
    z = np.zeros_like(x)
    im = None

    # Bottom right subplot (Population over time)
    time_array = np.arange(100)
    population = np.zeros(100)
    line = None

    # ---------- Animation Initialization ----------
    def init_all():
        nonlocal scatter, im, line
        # Left subplot: Predator/Prey
        ax_left = animator.axes[0]
        ax_left.set_xlim(0, 1)
        ax_left.set_ylim(0, 1)
        scatter = ax_left.scatter(pos[:, 0], pos[:, 1], c='red')
        
        # Top right subplot: Food Field
        ax_top = animator.axes[1]
        im = ax_top.imshow(z, extent=[0, 1, 0, 1], origin='lower', cmap='Greens', vmin=0, vmax=1)
        
        # Bottom right subplot: Population
        ax_bottom = animator.axes[2]
        ax_bottom.set_xlim(0, 100)
        ax_bottom.set_ylim(0, num_entities + 10)
        line, = ax_bottom.plot(time_array, population, color='blue')
        
        return scatter, im, line

    frame_counter = [0]  # mutable container to hold frame count

    def update_all(frame):
        nonlocal pos, vel, scatter, z, im, line, population
        # Update Left subplot: Predator/Prey (simple bouncing dots)
        pos += vel
        # Bounce off the walls
        for i in range(2):
            mask_low = pos[:, i] < 0
            mask_high = pos[:, i] > 1
            vel[mask_low | mask_high, i] *= -1
            pos[:, i] = np.clip(pos[:, i], 0, 1)
        scatter.set_offsets(pos)
        
        # Update Top right subplot: Food Field (sinusoidal wave)
        z = 0.5 + 0.5 * np.sin(2 * np.pi * (x + y + frame * 0.01))
        im.set_array(z)
        
        # Update Bottom right subplot: Population (simulate population oscillation)
        frame_counter[0] += 1
        # Shift the population data to the left
        population = np.roll(population, -1)
        # Simulate a population value that oscillates about the number of entities
        population[-1] = num_entities + 3 * np.sin(frame_counter[0] * 0.1)
        line.set_ydata(population)
        
        return scatter, im, line

    animator.set_animator(init_all, update_all, interval=100)
    animator.show()


if __name__ == "__main__":
    simulation_example()
