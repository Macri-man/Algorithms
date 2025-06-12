import numpy as np
class LSTM:
    def __init__(self, input_size, hidden_size):
        self.input_size = input_size
        self.hidden_size = hidden_size

        # Weights for input and hidden state
        self.Wf = np.random.randn(hidden_size, input_size) * 0.01  # Forget gate
        self.Wi = np.random.randn(hidden_size, input_size) * 0.01  # Input gate
        self.Wc = np.random.randn(hidden_size, input_size) * 0.01  # Cell state
        self.Wo = np.random.randn(hidden_size, input_size) * 0.01  # Output gate

        self.Uf = np.random.randn(hidden_size, hidden_size) * 0.01
        self.Ui = np.random.randn(hidden_size, hidden_size) * 0.01
        self.Uc = np.random.randn(hidden_size, hidden_size) * 0.01
        self.Uo = np.random.randn(hidden_size, hidden_size) * 0.01

        self.bf = np.zeros((hidden_size, 1))
        self.bi = np.zeros((hidden_size, 1))
        self.bc = np.zeros((hidden_size, 1))
        self.bo = np.zeros((hidden_size, 1))

    def forward(self, x, h_prev, c_prev):
        # Forget gate
        f_t = self.sigmoid(np.dot(self.Wf, x) + np.dot(self.Uf, h_prev) + self.bf)
        # Input gate
        i_t = self.sigmoid(np.dot(self.Wi, x) + np.dot(self.Ui, h_prev) + self.bi)
        # Cell gate
        C_hat_t = np.tanh(np.dot(self.Wc, x) + np.dot(self.Uc, h_prev) + self.bc)
        # Cell state
        c_t = f_t * c_prev + i_t * C_hat_t
        # Output gate
        o_t = self.sigmoid(np.dot(self.Wo, x) + np.dot(self.Uo, h_prev) + self.bo)
        # Hidden state
        h_t = o_t * np.tanh(c_t)

        return h_t, c_t, f_t, i_t, C_hat_t, o_t

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
class LSTMNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.lstm = LSTM(input_size, hidden_size)
        self.Wy = np.random.randn(output_size, hidden_size) * 0.01  # Output weights
        self.by = np.zeros((output_size, 1))  # Output bias

    def forward(self, inputs):
        h_prev = np.zeros((self.lstm.hidden_size, 1))  # Initial hidden state
        c_prev = np.zeros((self.lstm.hidden_size, 1))  # Initial cell state

        outputs = []
        for x in inputs:
            h_prev, c_prev, _, _, _, _ = self.lstm.forward(x.reshape(-1, 1), h_prev, c_prev)
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

# Create the LSTM model
lstm_network = LSTMNetwork(input_size, hidden_size, output_size)

# Test the forward pass with one sequence
sample_sequence = X[0]  # Take one sample sequence
output, _ = lstm_network.forward(sample_sequence)

# Print output for the sequence
print(f'Output shape: {output.shape}')
print(f'Output values: {output.flatten()}')
