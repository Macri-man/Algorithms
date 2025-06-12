import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class MultiPlotAnimator:
    def __init__(self, layout=(1, 2), figsize=(10, 5)):
        self.rows, self.cols = layout
        self.fig, self.axes = plt.subplots(self.rows, self.cols, figsize=figsize)

        # Flatten axes array to simplify handling
        if isinstance(self.axes, np.ndarray):
            self.axes = self.axes.flatten()
        else:
            self.axes = [self.axes]

        self.artists = []  # Plots to update

    def set_init_update_funcs(self, init_func, update_func, interval=100, frames=None):
        # One animator for all plots
        self.anim = animation.FuncAnimation(
            self.fig,
            update_func,
            init_func=init_func,
            interval=interval,
            blit=True,
            frames=frames,
            cache_frame_data=False
        )

    def show(self):
        plt.tight_layout()
        plt.show()


def predator_prey_food_sim():
    animator = MultiPlotAnimator(layout=(1, 2), figsize=(12, 5))

    # Subplot 1: Bouncing dots (predator/prey)
    num_dots = 20
    pos = np.random.rand(num_dots, 2)
    vel = (np.random.rand(num_dots, 2) - 0.5) * 0.05
    scatter = None

    # Subplot 2: Food waves
    x, y = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))
    z = np.zeros_like(x)
    im = None

    def init_all():
        nonlocal scatter, im
        # Init predator/prey
        ax1 = animator.axes[0]
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        scatter = ax1.scatter(pos[:, 0], pos[:, 1], c='red')

        # Init food
        ax2 = animator.axes[1]
        im = ax2.imshow(z, extent=[0, 1, 0, 1], origin='lower', cmap='Greens', vmin=0, vmax=1)

        return scatter, im

    def update_all(frame):
        nonlocal pos, vel, scatter, z, im

        # Update predator/prey
        pos += vel
        for d in range(2):
            mask_low = pos[:, d] < 0
            mask_high = pos[:, d] > 1
            vel[mask_low | mask_high, d] *= -1
            pos[:, d] = np.clip(pos[:, d], 0, 1)
        scatter.set_offsets(pos)

        # Update food (sinusoidal wave)
        z = 0.5 + 0.5 * np.sin(2 * np.pi * (x + y + frame * 0.01))
        im.set_array(z)

        return scatter, im

    animator.set_init_update_funcs(init_all, update_all, interval=100)
    animator.show()

if __name__ == "__main__":
    predator_prey_food_sim()
