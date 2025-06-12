import numpy as np
class RNN:
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.01):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        
        # Initialize weights
        self.Wxh = np.random.randn(hidden_size, input_size) * 0.01  # Input to hidden
        self.Whh = np.random.randn(hidden_size, hidden_size) * 0.01  # Hidden to hidden
        self.Why = np.random.randn(output_size, hidden_size) * 0.01  # Hidden to output
        
        # Initialize biases
        self.bh = np.zeros((hidden_size, 1))  # Hidden layer bias
        self.by = np.zeros((output_size, 1))  # Output layer bias
        
    def forward(self, inputs):
        self.h = np.zeros((self.hidden_size, 1))  # Initialize hidden state
        self.outputs = []
        
        for x in inputs:
            x = x.reshape(-1, 1)  # Reshape input to (input_size, 1)
            self.h = np.tanh(np.dot(self.Wxh, x) + np.dot(self.Whh, self.h) + self.bh)  # Hidden state
            y = np.dot(self.Why, self.h) + self.by  # Output
            self.outputs.append(y)
        
        return self.outputs
    
    def backward(self, inputs, targets):
        # Backward pass (simplified, no actual gradients calculation for the purpose of this example)
        # Here, you'd normally compute gradients and update weights accordingly
        pass
    
    def update_parameters(self):
        # Here, you'd normally update weights using gradients calculated in the backward pass
        pass
def generate_synthetic_data(num_samples=1000, sequence_length=5):
    X = np.random.rand(num_samples, sequence_length, 1)  # Random sequences
    y = (np.sum(X, axis=1) > (sequence_length / 2)).astype(int)  # Labels: 1 if sum > 2.5, else 0
    return X, y

X, y = generate_synthetic_data()
input_size = 1  # Input size (e.g., one feature per time step)
hidden_size = 5  # Number of hidden units
output_size = 1  # Binary classification (0 or 1)

# Create the RNN model
rnn = RNN(input_size, hidden_size, output_size)

# Test the forward pass with one sequence
sample_sequence = X[0]  # Take one sample sequence
output = rnn.forward(sample_sequence)

# Print output for the sequence
print(f'Output shape: {len(output)}')
print(f'Output values: {[o.flatten() for o in output]}')
