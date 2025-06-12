import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class MultiAnimator:
    def __init__(self, rows, cols, figsize=(10, 6)):
        self.rows = rows
        self.cols = cols
        self.fig, self.axes = plt.subplots(rows, cols, figsize=figsize)
        self.animations = []

        # Flatten the axes array for easy indexing
        if isinstance(self.axes, np.ndarray):
            self.axes = self.axes.flatten()
        else:
            self.axes = [self.axes]

    def add_animator(self, idx, init_func, update_func, interval=100, frames=None, blit=True):
        ax = self.axes[idx]
        anim = animation.FuncAnimation(
            self.fig,
            update_func,
            init_func=init_func,
            interval=interval,
            blit=blit,
            frames=frames,
            cache_frame_data=False  # Prevent unbounded cache warning
        )
        self.animations.append(anim)
        return anim

    def show(self):
        plt.tight_layout()
        plt.show()


def predator_prey_example():
    multi_anim = MultiAnimator(rows=1, cols=2, figsize=(12, 5))

    # Subplot 0: simple bouncing predators/prey
    num_entities = 15
    pos = np.random.rand(num_entities, 2)
    vel = (np.random.rand(num_entities, 2) - 0.5) * 0.05
    scatter = None

    def init_sim():
        nonlocal scatter
        ax = multi_anim.axes[0]
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        scatter = ax.scatter(pos[:, 0], pos[:, 1], c='blue')
        return scatter,

    def update_sim(frame):
        nonlocal pos, vel, scatter
        pos += vel
        # Bounce off walls
        for dim in range(2):
            out_of_bounds_low = pos[:, dim] < 0
            out_of_bounds_high = pos[:, dim] > 1
            vel[out_of_bounds_low | out_of_bounds_high, dim] *= -1
            pos[:, dim] = np.clip(pos[:, dim], 0, 1)

        scatter.set_offsets(pos)
        return scatter,

    multi_anim.add_animator(0, init_sim, update_sim, interval=50)

    # Subplot 1: prey growth like food (noise expansion)
    x, y = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))
    z = np.zeros_like(x)
    im = None

    def init_food():
        nonlocal im
        ax = multi_anim.axes[1]
        im = ax.imshow(z, extent=[0, 1, 0, 1], origin='lower', cmap='Greens', vmin=0, vmax=1)
        return im,

    def update_food(frame):
        nonlocal z, im
        # Make food grow over time like Perlin noise (mocked)
        z = 0.5 + 0.5 * np.sin(2 * np.pi * (x + y + frame * 0.01))
        im.set_array(z)
        return im,

    multi_anim.add_animator(1, init_food, update_food, interval=100)

    multi_anim.show()

if __name__ == "__main__":
    predator_prey_example()
