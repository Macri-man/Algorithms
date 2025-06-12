import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import numpy as np

class MultiPlotAnimator:
    def __init__(self, figsize=(10, 6)):
        self.fig = plt.figure(figsize=figsize)
        self.gs = gridspec.GridSpec(2, 2, width_ratios=[2, 1], height_ratios=[1, 1])

        # Create axes
        self.ax_left = self.fig.add_subplot(self.gs[:, 0])  # spans both rows
        self.ax_top_right = self.fig.add_subplot(self.gs[0, 1])
        self.ax_bottom_right = self.fig.add_subplot(self.gs[1, 1])
        self.axes = [self.ax_left, self.ax_top_right, self.ax_bottom_right]

        self.artists = []

    def set_init_update_funcs(self, init_func, update_func, interval=100, frames=None):
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
    animator = MultiPlotAnimator(figsize=(12, 6))

    # Left: Predator/Prey
    num_dots = 20
    pos = np.random.rand(num_dots, 2)
    vel = (np.random.rand(num_dots, 2) - 0.5) * 0.05
    scatter = None

    # Top right: Food wave
    x, y = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))
    z = np.zeros_like(x)
    im = None

    # Bottom right: Random line chart (population over time)
    t = np.arange(100)
    pop = np.zeros(100)
    line = None

    def init_all():
        nonlocal scatter, im, line
        # Predator/Prey
        ax1 = animator.ax_left
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.set_title("Predator/Prey")
        scatter = ax1.scatter(pos[:, 0], pos[:, 1], c='red')

        # Food
        ax2 = animator.ax_top_right
        ax2.set_title("Food Field")
        im = ax2.imshow(z, extent=[0, 1, 0, 1], origin='lower', cmap='Greens', vmin=0, vmax=1)

        # Population
        ax3 = animator.ax_bottom_right
        ax3.set_title("Population")
        ax3.set_xlim(0, 100)
        ax3.set_ylim(0, num_dots)
        line, = ax3.plot(t, pop, color='blue')

        return scatter, im, line

    frame_count = [0]  # workaround to allow updating pop

    def update_all(frame):
        nonlocal pos, vel, scatter, z, im, line, pop, frame_count

        # Move dots
        pos += vel
        for d in range(2):
            mask_low = pos[:, d] < 0
            mask_high = pos[:, d] > 1
            vel[mask_low | mask_high, d] *= -1
            pos[:, d] = np.clip(pos[:, d], 0, 1)
        scatter.set_offsets(pos)

        # Update food
        z = 0.5 + 0.5 * np.sin(2 * np.pi * (x + y + frame * 0.01))
        im.set_array(z)

        # Update population
        frame_count[0] += 1
        pop = np.roll(pop, -1)
        pop[-1] = num_dots + 3 * np.sin(frame_count[0] * 0.1)
        line.set_ydata(pop)

        return scatter, im, line

    animator.set_init_update_funcs(init_all, update_all, interval=100)
    animator.show()

if __name__ == "__main__":
    predator_prey_food_sim()

