import numpy as np
import matplotlib.pyplot as plt
import time

# Step 1: Generate linearly separable data
np.random.seed(int(time.time()))
num_points = 100
X = np.random.randn(num_points, 2)
y = np.where(X[:, 0] + X[:, 1] > 0, 1, 0)  # Linearly separable rule

# Step 2: Add bias term to input
X_bias = np.hstack([X, np.ones((X.shape[0], 1))])  # Add bias column

# Step 3: Perceptron implementation
class Perceptron:
    def __init__(self, learning_rate=0.1, n_iters=1000):
        self.lr = learning_rate
        self.n_iters = n_iters
        self.weights = None

    def activation(self, x):
        return np.where(x >= 0, 1, 0)

    def fit(self, X, y):
        self.weights = np.zeros(X.shape[1])
        for _ in range(self.n_iters):
            for xi, target in zip(X, y):
                output = self.activation(np.dot(xi, self.weights))
                error = target - output
                self.weights += self.lr * error * xi

    def predict(self, X):
        return self.activation(np.dot(X, self.weights))

# Step 4: Train perceptron
perceptron = Perceptron()
perceptron.fit(X_bias, y)

# Step 5: Plot data and decision boundary
def plot_decision_boundary(X, y, model):
    plt.figure(figsize=(8, 6))
    plt.scatter(X[y == 0][:, 0], X[y == 0][:, 1], color='red', label='Class 0')
    plt.scatter(X[y == 1][:, 0], X[y == 1][:, 1], color='blue', label='Class 1')

    # Decision boundary: w1*x + w2*y + b = 0 => y = -(w1*x + b)/w2
    w = model.weights
    x_vals = np.linspace(X[:, 0].min(), X[:, 0].max(), 100)
    y_vals = -(w[0] * x_vals + w[2]) / w[1]
    plt.plot(x_vals, y_vals, color='green', linewidth=2, label='Decision Boundary')

    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title("Perceptron Decision Boundary")
    plt.legend()
    plt.grid(True)
    plt.show()

plot_decision_boundary(X, y, perceptron)
