import numpy as np
class ConvLayer:
    def __init__(self, num_filters, filter_size, input_depth):
        self.num_filters = num_filters
        self.filter_size = filter_size
        self.input_depth = input_depth
        
        # Initialize weights and biases
        self.filters = np.random.randn(num_filters, input_depth, filter_size, filter_size) * 0.01
        self.biases = np.zeros((num_filters, 1))

    def forward(self, input):
        self.input = input
        self.input_height, self.input_width, self.input_depth = input.shape
        self.output_height = self.input_height - self.filter_size + 1
        self.output_width = self.input_width - self.filter_size + 1
        self.output = np.zeros((self.output_height, self.output_width, self.num_filters))

        for f in range(self.num_filters):
            for i in range(self.output_height):
                for j in range(self.output_width):
                    region = input[i:i+self.filter_size, j:j+self.filter_size, :]
                    self.output[i, j, f] = np.sum(region * self.filters[f]) + self.biases[f]

        return self.output
class ReLU:
    def forward(self, input):
        return np.maximum(0, input)
class MaxPool:
    def __init__(self, size):
        self.size = size

    def forward(self, input):
        self.input = input
        self.input_height, self.input_width, input_depth = input.shape
        self.output_height = self.input_height // self.size
        self.output_width = self.input_width // self.size
        self.output = np.zeros((self.output_height, self.output_width, input_depth))

        for i in range(self.output_height):
            for j in range(self.output_width):
                region = input[i*self.size:(i+1)*self.size, j*self.size:(j+1)*self.size, :]
                self.output[i, j, :] = np.max(region, axis=(0, 1))

        return self.output
class FullyConnectedLayer:
    def __init__(self, input_size, output_size):
        self.weights = np.random.randn(input_size, output_size) * 0.01
        self.biases = np.zeros((output_size, 1))

    def forward(self, input):
        self.input = input
        return np.dot(self.weights.T, input) + self.biases
class CNN:
    def __init__(self):
        self.conv1 = ConvLayer(num_filters=8, filter_size=3, input_depth=3)
        self.relu1 = ReLU()
        self.pool1 = MaxPool(size=2)
        self.fc1 = FullyConnectedLayer(input_size=8 * 13 * 13, output_size=10)  # Example output for 10 classes

    def forward(self, input):
        out = self.conv1.forward(input)
        out = self.relu1.forward(out)
        out = self.pool1.forward(out)
        out = out.flatten().reshape(-1, 1)  # Flatten for fully connected layer
        out = self.fc1.forward(out)
        return out
def generate_synthetic_data(num_samples=1000):
    X = np.random.rand(num_samples, 32, 32, 3)  # 32x32 RGB images
    y = np.random.randint(0, 10, size=(num_samples, 1))  # Random labels for 10 classes
    return X, y

X, y = generate_synthetic_data()
cnn = CNN()

# Test the forward pass with one image
sample_image = X[0]  # Take one sample
output = cnn.forward(sample_image)

print(f'Output shape: {output.shape}')
print(f'Output values: {output.flatten()}')
