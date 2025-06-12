import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.patches as mpatches
import matplotlib.animation as animation


class ForestFireSimulation:
    EMPTY = 0
    TREE = 1
    FIRE = 2

    def __init__(self, size=100, p=0.01, f=0.001, moisture=0.3, wind=(0, 0)):
        self.size = size
        self.p = p
        self.f = f
        self.moisture = moisture
        self.wind = wind
        self.grid = np.zeros((size, size), dtype=int)

    def step(self):
        # Forest growth
        self._grow_forest()

        # Fire spread
        self._spread_fire()

        # Fire decay (moisture effect)
        self._decay_fire()

    def _grow_forest(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] == self.EMPTY and np.random.random() < self.p:
                    self.grid[i, j] = self.TREE

    def _spread_fire(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] == self.TREE and np.random.random() < self.f:
                    if self.is_fire_adjacent(i, j):
                        self.grid[i, j] = self.FIRE

    def _decay_fire(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] == self.FIRE and np.random.random() > self.moisture:
                    self.grid[i, j] = self.EMPTY

    def is_fire_adjacent(self, i, j):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for di, dj in directions:
            ni, nj = i + di + self.wind[0], j + dj + self.wind[1]
            if 0 <= ni < self.size and 0 <= nj < self.size and self.grid[ni, nj] == self.FIRE:
                return True
        return False


def setup_plot(sim):
    fig, ((ax_sim, ax_stats), (ax_controls, ax_legend)) = plt.subplots(
        2, 2, figsize=(10, 8), gridspec_kw={'width_ratios': [3, 1], 'height_ratios': [3, 1]}
    )
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.15, top=0.9, hspace=0.5)

    # Simulation display (left side)
    cmap = plt.get_cmap('viridis', 3)
    im = ax_sim.imshow(sim.grid, cmap=cmap, vmin=0, vmax=2)
    ax_sim.set_title("Interactive Forest Fire Simulation")
    ax_sim.axis('off')

    # Legend (top-right)
    legend_patches = [
        mpatches.Patch(color=cmap(0), label='Empty'),
        mpatches.Patch(color=cmap(1), label='Tree'),
        mpatches.Patch(color=cmap(2), label='Fire')
    ]
    ax_legend.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3)

    # Stats panel (right side)
    stat_text = ax_stats.text(0.02, 0.98, "", transform=ax_stats.transAxes,
                             verticalalignment='top', bbox=dict(facecolor='white', alpha=0.6))
    ax_stats.axis('off')

    # Fire stats over time plot (bottom)
    fire_data = []
    fire_line, = ax_controls.plot([], [], color='red', label='🔥 Fire %')
    ax_controls.set_xlim(0, 100)
    ax_controls.set_ylim(0, 100)
    ax_controls.set_ylabel("Fire %")
    ax_controls.set_xlabel("Step")
    ax_controls.legend()

    return fig, ax_sim, ax_stats, ax_controls, ax_legend, stat_text, fire_line, fire_data


def setup_sliders(sim):
    slider_axes = {
        "p": plt.axes([0.1, 0.02, 0.65, 0.03]),
        "f": plt.axes([0.1, 0.06, 0.65, 0.03]),
        "moisture": plt.axes([0.1, 0.1, 0.65, 0.03]),
        "wind_x": plt.axes([0.1, 0.14, 0.65, 0.03]),
        "wind_y": plt.axes([0.1, 0.18, 0.65, 0.03])
    }

    sliders = {
        "p": Slider(slider_axes["p"], 'Growth (p)', 0.0, 0.1, valinit=sim.p, valstep=0.001),
        "f": Slider(slider_axes["f"], 'Fire (f)', 0.0, 0.01, valinit=sim.f, valstep=0.0001),
        "moisture": Slider(slider_axes["moisture"], 'Moisture', 0.0, 1.0, valinit=sim.moisture, valstep=0.01),
        "wind_x": Slider(slider_axes["wind_x"], 'Wind X', -1, 1, valinit=sim.wind[0], valstep=1),
        "wind_y": Slider(slider_axes["wind_y"], 'Wind Y', -1, 1, valinit=sim.wind[1], valstep=1),
    }

    return sliders


def update_params(sliders, sim):
    sim.p = sliders["p"].val
    sim.f = sliders["f"].val
    sim.moisture = sliders["moisture"].val
    sim.wind = (int(sliders["wind_x"].val), int(sliders["wind_y"].val))


def setup_controls():
    is_paused = [False]

    def toggle_pause(event):
        is_paused[0] = not is_paused[0]
        btn.label.set_text("⏸ Pause" if not is_paused[0] else "▶ Play")

    btn_ax = plt.axes([0.75, 0.02, 0.1, 0.04])
    btn = Button(btn_ax, "⏸ Pause")
    btn.on_clicked(toggle_pause)

    return is_paused, btn


def animate(frame, sim, im, fire_line, ax_controls, stat_text, fire_data, is_paused, step_count):
    if not is_paused[0]:
        sim.step()
        im.set_array(sim.grid)

        # Stats update
        total = sim.size * sim.size
        empty = np.count_nonzero(sim.grid == ForestFireSimulation.EMPTY)
        tree = np.count_nonzero(sim.grid == ForestFireSimulation.TREE)
        fire = np.count_nonzero(sim.grid == ForestFireSimulation.FIRE)
        fire_pct = (fire / total) * 100

        stat_text.set_text(
            f"🌲 Trees: {tree/total:.1%} | 🔥 Fires: {fire/total:.1%} | ⬛ Empty: {empty/total:.1%}"
        )

        # Fire plot update
        fire_data.append(fire_pct)
        fire_line.set_data(range(len(fire_data)), fire_data)
        ax_controls.set_xlim(0, max(100, len(fire_data)))
        ax_controls.set_ylim(0, max(10, max(fire_data) + 5))

        step_count[0] += 1

    return [im, fire_line, stat_text]


def main():
    sim = ForestFireSimulation()

    fig, ax_sim, ax_stats, ax_controls, ax_legend, stat_text, fire_line, fire_data = setup_plot(sim)
    sliders = setup_sliders(sim)
    is_paused, btn = setup_controls()

    for slider in sliders.values():
        slider.on_changed(lambda val: update_params(sliders, sim))

    step_count = [0]

    ani = animation.FuncAnimation(
        fig, lambda frame: animate(frame, sim, ax_sim.imshow(sim.grid), fire_line, ax_controls, stat_text, fire_data, is_paused, step_count),
        interval=100, blit=False
    )

    plt.show()


if __name__ == "__main__":
    main()
