import numpy as np
class FeedforwardNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.01):
        # Initialize weights and biases
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        
        # Weights
        self.W1 = np.random.rand(self.input_size, self.hidden_size) * 0.01
        self.W2 = np.random.rand(self.hidden_size, self.output_size) * 0.01
        
        # Biases
        self.b1 = np.zeros((1, self.hidden_size))
        self.b2 = np.zeros((1, self.output_size))

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def sigmoid_derivative(self, z):
        return z * (1 - z)

    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2

    def backward(self, X, y):
        m = y.shape[0]
        
        # Calculate error
        error = self.a2 - y
        
        # Backpropagation
        dW2 = (1/m) * np.dot(self.a1.T, error * self.sigmoid_derivative(self.a2))
        db2 = (1/m) * np.sum(error * self.sigmoid_derivative(self.a2), axis=0, keepdims=True)
        
        error_hidden = np.dot(error, self.W2.T)
        dW1 = (1/m) * np.dot(X.T, error_hidden * self.sigmoid_derivative(self.a1))
        db1 = (1/m) * np.sum(error_hidden * self.sigmoid_derivative(self.a1), axis=0, keepdims=True)
        
        # Update weights and biases
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2

    def train(self, X, y, epochs):
        for epoch in range(epochs):
            self.forward(X)
            self.backward(X, y)
            if epoch % 100 == 0:
                loss = np.mean(np.square(y - self.a2))
                print(f'Epoch {epoch}, Loss: {loss:.4f}')
def generate_data(num_samples=1000):
    np.random.seed(42)
    X = np.random.rand(num_samples, 2)  # 2 features
    y = (X[:, 0] + X[:, 1] > 1).astype(int).reshape(-1, 1)  # Label is 1 if sum of features > 1
    return X, y

X, y = generate_data()
input_size = 2
hidden_size = 5  # Number of neurons in the hidden layer
output_size = 1  # Output is binary (0 or 1)

# Create the model
model = FeedforwardNeuralNetwork(input_size, hidden_size, output_size)

# Train the model
model.train(X, y, epochs=1000)
def predict(model, X):
    output = model.forward(X)
    return (output > 0.5).astype(int)

# Test predictions
test_data = np.array([[0.3, 0.7], [0.9, 0.1]])
predictions = predict(model, test_data)
print(f'Predictions for {test_data}: {predictions.flatten()}')
