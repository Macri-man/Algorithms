import numpy as np
import matplotlib.pyplot as plt
from numpy import exp

class ShapePlotter:
    def __init__(self):
        self.t = np.linspace(0, 12 * np.pi, 1000)

    def compute_heart_shape(self):
        x = 16 * np.sin(self.t)**3
        y = 13 * np.cos(self.t) - 5 * np.cos(2 * self.t) - 2 * np.cos(3 * self.t) - np.cos(4 * self.t)
        return x, y

    def compute_butterfly_shape(self):
        factor = exp(np.cos(self.t)) - 2 * np.cos(4 * self.t) + np.sin(self.t / 12)**5
        x = np.sin(self.t) * factor
        y = np.cos(self.t) * factor
        return x, y

    def plot_shapes(self):
        x_heart, y_heart = self.compute_heart_shape()
        x_butterfly, y_butterfly = self.compute_butterfly_shape()

        # Heart Shape in its own figure
        plt.figure(figsize=(6, 6))
        plt.plot(x_heart, y_heart, color='red')
        plt.title("Heart Shape")
        plt.axis('equal')
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)

        # Butterfly Shape in its own figure
        plt.figure(figsize=(6, 6))
        plt.plot(x_butterfly, y_butterfly, color='blue')
        plt.title("Butterfly Shape")
        plt.axis('equal')
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)

        plt.show()

def main():
    plotter = ShapePlotter()
    plotter.plot_shapes()

if __name__ == "__main__":
    main()
