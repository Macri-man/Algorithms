import numpy as np
class GRU:
    def __init__(self, input_size, hidden_size):
        self.input_size = input_size
        self.hidden_size = hidden_size

        # Weights for the update gate, reset gate, and hidden state
        self.Wz = np.random.randn(hidden_size, input_size) * 0.01  # Update gate
        self.Uz = np.random.randn(hidden_size, hidden_size) * 0.01
        self.bz = np.zeros((hidden_size, 1))

        self.Wr = np.random.randn(hidden_size, input_size) * 0.01  # Reset gate
        self.Ur = np.random.randn(hidden_size, hidden_size) * 0.01
        self.br = np.zeros((hidden_size, 1))

        self.Wh = np.random.randn(hidden_size, input_size) * 0.01  # Hidden state
        self.Uh = np.random.randn(hidden_size, hidden_size) * 0.01
        self.bh = np.zeros((hidden_size, 1))

    def forward(self, x, h_prev):
        # Update gate
        z_t = self.sigmoid(np.dot(self.Wz, x) + np.dot(self.Uz, h_prev) + self.bz)
        # Reset gate
        r_t = self.sigmoid(np.dot(self.Wr, x) + np.dot(self.Ur, h_prev) + self.br)
        # Candidate hidden state
        h_tilde = np.tanh(np.dot(self.Wh, x) + np.dot(self.Uh, r_t * h_prev) + self.bh)
        # Current hidden state
        h_t = (1 - z_t) * h_prev + z_t * h_tilde

        return h_t, z_t, r_t, h_tilde

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
class GRUNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.gru = GRU(input_size, hidden_size)
        self.Wy = np.random.randn(output_size, hidden_size) * 0.01  # Output weights
        self.by = np.zeros((output_size, 1))  # Output bias

    def forward(self, inputs):
        h_prev = np.zeros((self.gru.hidden_size, 1))  # Initial hidden state

        outputs = []
        for x in inputs:
            h_prev, _, _, _ = self.gru.forward(x.reshape(-1, 1), h_prev)
            outputs.append(h_prev)

        # Output layer
        y = np.dot(self.Wy, h_prev) + self.by
        return y, outputs
def generate_synthetic_data(num_samples=1000, sequence_length=5):
    X = np.random.rand(num_samples, sequence_length, 1)  # Random sequences
    y = (np.sum(X, axis=1) > (sequence_length / 2)).astype(int)  # Labels: 1 if sum > 2.5, else 0
    return X, y

X, y = generate_synthetic_data()
input_size = 1  # Input size (e.g., one feature per time step)
hidden_size = 5  # Number of hidden units
output_size = 1  # Binary classification (0 or 1)

# Create the GRU model
gru_network = GRUNetwork(input_size, hidden_size, output_size)

# Test the forward pass with one sequence
sample_sequence = X[0]  # Take one sample sequence
output, _ = gru_network.forward(sample_sequence)

# Print output for the sequence
print(f'Output shape: {output.shape}')
print(f'Output values: {output.flatten()}')
