import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter


# 1D Cellular Automaton
class OneDCA:
    def __init__(self, rule_number=30, width=101, generations=100):
        self.rule_number = rule_number
        self.width = width
        self.generations = generations
        self.rule = self._rule_to_binary(rule_number)
        self.grid = np.zeros((generations, width), dtype=int)
        self.grid[0, width // 2] = 1  # Initial seed

    def _rule_to_binary(self, rule):
        return [int(x) for x in f"{rule:08b}"][::-1]

    def _apply_rule(self, left, center, right):
        index = 4 * left + 2 * center + right
        return self.rule[index]

    def evolve(self):
        for t in range(1, self.generations):
            for i in range(1, self.width - 1):
                l, c, r = self.grid[t-1, i-1:i+2]
                self.grid[t, i] = self._apply_rule(l, c, r)

    def save_animation(self, filename="1d_ca.mp4"):
        self.evolve()
        fig, ax = plt.subplots()
        img = ax.imshow(self.grid[:1], cmap="binary", aspect='auto')
        ax.axis("off")

        def update(frame):
            img.set_data(self.grid[:frame+1])
            return [img]

        ani = animation.FuncAnimation(fig, update, frames=self.generations, blit=True)

        writer = FFMpegWriter(fps=15)
        ani.save(filename, writer=writer)
        plt.close(fig)


# 2D Cellular Automaton (Conway's Game of Life)
class TwoDCA:
    def __init__(self, size=50, steps=100):
        self.size = size
        self.steps = steps
        self.grid = np.random.choice([0, 1], size=(size, size), p=[0.8, 0.2])
        self.frames = []

    def _step(self):
        neighbors = sum(np.roll(np.roll(self.grid, i, 0), j, 1)
                        for i in (-1, 0, 1) for j in (-1, 0, 1)
                        if (i != 0 or j != 0))
        self.grid = ((neighbors == 3) | ((self.grid == 1) & (neighbors == 2))).astype(int)

    def save_animation(self, filename="2d_ca.mp4"):
        fig, ax = plt.subplots()
        img = ax.imshow(self.grid, cmap="binary")
        ax.axis("off")

        def update(frame):
            self._step()
            img.set_data(self.grid)
            return [img]

        ani = animation.FuncAnimation(fig, update, frames=self.steps, blit=True)

        writer = FFMpegWriter(fps=10)
        ani.save(filename, writer=writer)
        plt.close(fig)


# Main function to run and save animations
def main():
    print("Saving 1D Cellular Automaton...")
    ca1d = OneDCA(rule_number=30, width=101, generations=100)
    ca1d.save_animation("1d_ca.mp4")

    print("Saving 2D Cellular Automaton...")
    ca2d = TwoDCA(size=50, steps=100)
    ca2d.save_animation("2d_ca.mp4")


if __name__ == "__main__":
    main()
