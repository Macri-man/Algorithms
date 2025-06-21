import numpy as np
from sklearn.datasets import make_moons, make_circles
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

class DeepNeuralNetwork:
    def __init__(self, layers, learning_rate=0.01):
        self.layers = layers
        self.learning_rate = learning_rate
        self.weights = []
        self.biases = []

        for i in range(len(layers) - 1):
            w = np.random.randn(layers[i], layers[i+1]) * np.sqrt(2. / layers[i])
            b = np.zeros((1, layers[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def relu(self, x):
        return np.maximum(0, x)

    def relu_derivative(self, x):
        return (x > 0).astype(float)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def forward(self, X):
        self.Z = []
        self.A = [X]

        for i in range(len(self.weights) - 1):
            Z = np.dot(self.A[-1], self.weights[i]) + self.biases[i]
            A = self.relu(Z)
            self.Z.append(Z)
            self.A.append(A)

        Z = np.dot(self.A[-1], self.weights[-1]) + self.biases[-1]
        A = self.sigmoid(Z)
        self.Z.append(Z)
        self.A.append(A)
        return A

    def backward(self, y):
        m = y.shape[0]
        dA = self.A[-1] - y

        for i in reversed(range(len(self.weights))):
            dZ = dA * (self.sigmoid_derivative(self.A[i+1]) if i == len(self.weights) - 1 else self.relu_derivative(self.Z[i]))
            dW = np.dot(self.A[i].T, dZ) / m
            db = np.sum(dZ, axis=0, keepdims=True) / m

            dA = np.dot(dZ, self.weights[i].T)

            self.weights[i] -= self.learning_rate * dW
            self.biases[i] -= self.learning_rate * db

    def compute_loss(self, y, y_pred):
        return np.mean((y - y_pred) ** 2)

    def train(self, X, y, epochs=10000):
        for epoch in range(epochs):
            y_pred = self.forward(X)
            loss = self.compute_loss(y, y_pred)
            self.backward(y)
            if epoch % 1000 == 0:
                print(f"Epoch {epoch} - Loss: {loss:.4f}")

    def predict(self, X):
        y_pred = self.forward(X)
        return (y_pred > 0.5).astype(int)

X = np.array([[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]])

y = np.array([[0], [1], [1], [0]])

X, y = make_moons(n_samples=1000, noise=0.2)
# X, y = make_circles(n_samples=1000, noise=0.1, factor=0.5)
y = y.reshape(-1, 1)  # Shape like (1000, 1)

net = DeepNeuralNetwork([2, 6, 4, 1], learning_rate=0.1)
net.train(X, y, epochs=10000)
print("Predictions:")
print(net.predict(X))

def plot_decision_boundary(model, X, y):
    h = 0.01
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    grid = np.c_[xx.ravel(), yy.ravel()]
    Z = model.predict(grid)
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y.flatten(), edgecolors='k', cmap=plt.cm.Spectral)
    plt.title("Decision Boundary")
    plt.show()

plot_decision_boundary(net, X, y)