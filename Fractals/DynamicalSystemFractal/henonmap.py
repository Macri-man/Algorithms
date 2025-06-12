import matplotlib.pyplot as plt
import random
import time

class HenonMap:
    def __init__(self, a=None, b=None, x0=None, y0=None, n_points=10000, random_seed=None, threshold=1e10):
        # Use time as seed if none provided; seed in milliseconds mod 2**32 for reproducibility.
        if random_seed is None:
            random_seed = int(time.time() * 1000) % (2**32)
        random.seed(random_seed)
        self.seed = random_seed  # Save seed for reference

        # Randomize parameters using tighter ranges for typical Henon map behavior.
        self.a = a if a is not None else random.uniform(1.2, 1.4)
        self.b = b if b is not None else random.uniform(0.2, 0.4)
        self.x0 = x0 if x0 is not None else random.uniform(-1, 1)
        self.y0 = y0 if y0 is not None else random.uniform(-1, 1)
        self.n_points = n_points
        self.threshold = threshold  # Threshold to catch divergence
        self.xs = []
        self.ys = []

    def generate(self):
        x, y = self.x0, self.y0
        self.xs, self.ys = [], []
        
        for i in range(self.n_points):
            try:
                x_new = 1 - self.a * x**2 + y
                y_new = self.b * x
            except OverflowError:
                print(f"OverflowError encountered at iteration {i}. Stopping iterations.")
                break

            # Check if the new value is too high (potential divergence)
            if abs(x_new) > self.threshold or abs(y_new) > self.threshold:
                print(f"Value exceeded threshold at iteration {i}. Stopping iterations.")
                break

            x, y = x_new, y_new
            self.xs.append(x)
            self.ys.append(y)

    def plot(self):
        # Generate if not already done
        if not self.xs or not self.ys:
            self.generate()
        plt.figure(figsize=(8, 6))
        plt.plot(self.xs, self.ys, '.', markersize=0.5, color='black')
        plt.title(f"Hénon Map (a={self.a:.3f}, b={self.b:.3f}) | Seed={self.seed}")
        plt.grid(True)
        plt.show()

# Example usage
if __name__ == '__main__':
    henon = HenonMap()
    henon.generate()
    henon.plot()
