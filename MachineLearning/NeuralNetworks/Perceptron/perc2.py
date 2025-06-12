import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# Generate data (same as before)
np.random.seed(int(time.time()))
num_points = 150
X = np.random.randn(num_points, 2)
y = np.where(X[:, 0] + X[:, 1] > 0, 1, 0)
X_bias = np.hstack([X, np.ones((X.shape[0], 1))])  # Add bias

class Perceptron:
    def __init__(self, learning_rate=0.1, n_iters=10):
        self.lr = learning_rate
        self.n_iters = n_iters
        self.weights = np.zeros(X_bias.shape[1])
        self.weights_history = []

    def activation(self, x):
        return np.where(x >= 0, 1, 0)

    def fit(self, X, y):
        for _ in range(self.n_iters):
            for xi, target in zip(X, y):
                output = self.activation(np.dot(xi, self.weights))
                error = target - output
                self.weights += self.lr * error * xi
            self.weights_history.append(self.weights.copy())  # save weights after each epoch

    def predict(self, X):
        return self.activation(np.dot(X, self.weights))

# Train perceptron and save weights at each epoch
perceptron = Perceptron(n_iters=25)
perceptron.fit(X_bias, y)

# Setup plot
fig, ax = plt.subplots(figsize=(8, 6))
colors = ['red' if label == 0 else 'blue' for label in y]
scatter = ax.scatter(X[:, 0], X[:, 1], c=colors)
line, = ax.plot([], [], 'g-', linewidth=2, label='Decision Boundary')

ax.set_xlim(X[:,0].min() - 1, X[:,0].max() + 1)
ax.set_ylim(X[:,1].min() - 1, X[:,1].max() + 1)
ax.set_xlabel("x1")
ax.set_ylabel("x2")
ax.set_title("Perceptron Training Animation")
ax.legend()
ax.grid(True)

def update(frame):
    w = perceptron.weights_history[frame]
    x_vals = np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 100)
    # Avoid division by zero if w[1] is 0
    if w[1] != 0:
        y_vals = -(w[0] * x_vals + w[2]) / w[1]
    else:
        y_vals = np.full_like(x_vals, -w[2])  # just horizontal line at -b

    line.set_data(x_vals, y_vals)
    ax.set_title(f"Perceptron Training Animation - Epoch {frame + 1}")
    return line,

ani = FuncAnimation(fig, update, frames=len(perceptron.weights_history), interval=500, repeat=False)

plt.show()
