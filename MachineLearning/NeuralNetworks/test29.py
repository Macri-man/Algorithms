import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def relu(Z):
    return np.maximum(0, Z)

def relu_derivative(Z):
    return (Z > 0).astype(float)

def softmax(Z):
    expZ = np.exp(Z - np.max(Z, axis=1, keepdims=True))
    return expZ / np.sum(expZ, axis=1, keepdims=True)

def cross_entropy(y_true, y_pred):
    n = y_true.shape[0]
    log_probs = -np.log(y_pred[range(n), y_true])
    return np.mean(log_probs)

def one_hot(y, num_classes):
    return np.eye(num_classes)[y]

class NeuralNetwork:
    def __init__(self, layers, learning_rate=0.1):
        self.layers = layers
        self.learning_rate = learning_rate
        self.weights = []
        self.biases = []

        for i in range(len(layers) - 1):
            w = np.random.randn(layers[i], layers[i+1]) * np.sqrt(2. / layers[i])
            b = np.zeros((1, layers[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def forward(self, X):
        self.Z = []
        self.A = [X]

        for i in range(len(self.weights) - 1):
            Z = self.A[-1] @ self.weights[i] + self.biases[i]
            A = relu(Z)
            self.Z.append(Z)
            self.A.append(A)

        Z = self.A[-1] @ self.weights[-1] + self.biases[-1]
        A = softmax(Z)
        self.Z.append(Z)
        self.A.append(A)
        return A

    def backward(self, y):
        m = y.shape[0]
        y_onehot = one_hot(y, self.layers[-1])
        dZ = self.A[-1] - y_onehot

        for i in reversed(range(len(self.weights))):
            dW = self.A[i].T @ dZ / m
            db = np.mean(dZ, axis=0, keepdims=True)
            if i > 0:
                dA = dZ @ self.weights[i].T
                dZ = dA * relu_derivative(self.Z[i-1])
            self.weights[i] -= self.learning_rate * dW
            self.biases[i] -= self.learning_rate * db

    def train(self, X, y, epochs=1000):
        for epoch in range(epochs):
            y_pred = self.forward(X)
            loss = cross_entropy(y, y_pred)
            self.backward(y)
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss:.4f}")

    def predict(self, X):
        y_pred = self.forward(X)
        return np.argmax(y_pred, axis=1)

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
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', cmap=plt.cm.Spectral)
    plt.title("Decision Boundary")
    plt.show()

def main():
    X, y = make_moons(n_samples=1000, noise=0.2, random_state=42)
    X = StandardScaler().fit_transform(X)

    model = NeuralNetwork([2, 10, 8, 2], learning_rate=0.1)  # 2 output neurons for binary classification
    model.train(X, y, epochs=2000)

    preds = model.predict(X)
    print("Predictions (first 10):", preds[:10])
    print("True labels (first 10):", y[:10])

    plot_decision_boundary(model, X, y)

if __name__ == "__main__":
    main()
