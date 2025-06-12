import numpy as np
import matplotlib.pyplot as plt
class Autoencoder:
    def __init__(self, input_size, hidden_size, learning_rate=0.01):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.learning_rate = learning_rate

        # Initialize weights and biases for encoder
        self.W_enc = np.random.randn(hidden_size, input_size) * 0.01
        self.b_enc = np.zeros((hidden_size, 1))

        # Initialize weights and biases for decoder
        self.W_dec = np.random.randn(input_size, hidden_size) * 0.01
        self.b_dec = np.zeros((input_size, 1))

    def encode(self, x):
        return self.relu(np.dot(self.W_enc, x) + self.b_enc)

    def decode(self, z):
        return self.sigmoid(np.dot(self.W_dec, z) + self.b_dec)

    def forward(self, x):
        self.encoded = self.encode(x)
        self.reconstructed = self.decode(self.encoded)
        return self.reconstructed

    def relu(self, z):
        return np.maximum(0, z)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def loss(self, x, y):
        return np.mean(np.square(x - y))  # Mean squared error

    def train(self, data, epochs, batch_size):
        for epoch in range(epochs):
            for i in range(0, data.shape[0], batch_size):
                batch = data[i:i + batch_size]

                # Forward pass
                reconstructed = self.forward(batch.T)

                # Compute loss
                current_loss = self.loss(batch.T, reconstructed)
                
                # Backpropagation
                self.backpropagate(batch.T, reconstructed)

            if epoch % 100 == 0:
                print(f'Epoch {epoch}, Loss: {current_loss:.4f}')

    def backpropagate(self, x, y):
        # Calculate the gradients using backpropagation
        d_loss = 2 * (y - x) / x.shape[1]

        # Update decoder weights and biases
        d_dec = d_loss * self.sigmoid_derivative(y)
        self.W_dec -= self.learning_rate * np.dot(d_dec, self.encoded.T)
        self.b_dec -= self.learning_rate * np.sum(d_dec, axis=1, keepdims=True)

        # Backpropagate to encoder
        d_encoded = np.dot(self.W_dec.T, d_dec)
        d_enc = d_encoded * self.relu_derivative(self.encoded)
        
        # Update encoder weights and biases
        self.W_enc -= self.learning_rate * np.dot(d_enc, x.T)
        self.b_enc -= self.learning_rate * np.sum(d_enc, axis=1, keepdims=True)

    def sigmoid_derivative(self, z):
        return z * (1 - z)

    def relu_derivative(self, z):
        return (z > 0).astype(float)
def generate_synthetic_data(num_samples=1000, input_size=20):
    return np.random.rand(num_samples, input_size)  # Random dataset

real_data = generate_synthetic_data()
input_size = 20  # Input dimension
hidden_size = 10  # Size of the compressed representation
learning_rate = 0.01

# Create the Autoencoder
autoencoder = Autoencoder(input_size=input_size, hidden_size=hidden_size, learning_rate=learning_rate)

# Train the Autoencoder
autoencoder.train(real_data, epochs=1000, batch_size=32)
# Test the Autoencoder on a sample
sample_data = real_data[0]  # Take the first sample
reconstructed_sample = autoencoder.forward(sample_data.reshape(-1, 1))

# Plot the original and reconstructed data
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title("Original Data")
plt.bar(range(input_size), sample_data.flatten())
plt.subplot(1, 2, 2)
plt.title("Reconstructed Data")
plt.bar(range(input_size), reconstructed_sample.flatten())
plt.show()
