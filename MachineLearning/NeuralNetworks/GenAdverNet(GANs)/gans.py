import numpy as np
import matplotlib.pyplot as plt
class Generator:
    def __init__(self, input_dim, output_dim):
        self.input_dim = input_dim
        self.output_dim = output_dim
        
        # Weights for generator
        self.W1 = np.random.randn(output_dim, input_dim) * 0.01  # Hidden layer weights
        self.b1 = np.zeros((output_dim, 1))  # Hidden layer bias

    def forward(self, z):
        h = self.relu(np.dot(self.W1, z) + self.b1)  # Hidden layer
        return h  # Output layer (generated data)

    def relu(self, z):
        return np.maximum(0, z)

class Discriminator:
    def __init__(self, input_dim):
        self.input_dim = input_dim
        
        # Weights for discriminator
        self.W2 = np.random.randn(1, input_dim) * 0.01  # Output layer weights
        self.b2 = np.zeros((1, 1))  # Output layer bias

    def forward(self, x):
        return self.sigmoid(np.dot(self.W2, x) + self.b2)  # Probability of being real

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
class GAN:
    def __init__(self, generator, discriminator, learning_rate=0.001):
        self.generator = generator
        self.discriminator = discriminator
        self.learning_rate = learning_rate

    def train(self, real_data, epochs, batch_size):
        for epoch in range(epochs):
            for _ in range(real_data.shape[0] // batch_size):
                # Generate random noise
                z = np.random.randn(self.generator.input_dim, batch_size)

                # Generate fake data
                fake_data = self.generator.forward(z)

                # Get real data batch
                real_data_batch = real_data[np.random.randint(0, real_data.shape[0], size=batch_size)]

                # Train the discriminator
                d_loss_real = self.discriminator.forward(real_data_batch.T)
                d_loss_fake = self.discriminator.forward(fake_data.T)

                # Compute loss for discriminator
                d_loss = -(np.mean(np.log(d_loss_real)) + np.mean(np.log(1 - d_loss_fake)))

                # Train the generator
                g_loss = self.discriminator.forward(fake_data.T)

                # Update parameters (gradient descent step)
                self.update_parameters(real_data_batch, fake_data, d_loss_real, d_loss_fake, g_loss)

            if epoch % 100 == 0:
                print(f'Epoch {epoch}, D Loss: {d_loss}, G Loss: {g_loss.mean()}')

    def update_parameters(self, real_data, fake_data, d_loss_real, d_loss_fake, g_loss):
        # Simplified parameter updates
        self.discriminator.W2 -= self.learning_rate * (d_loss_real.mean() - d_loss_fake.mean()) * real_data.T
        self.generator.W1 -= self.learning_rate * g_loss.mean() * fake_data.T
def generate_synthetic_data(num_samples=1000):
    return np.random.normal(loc=0, scale=1, size=(num_samples, 1))

real_data = generate_synthetic_data()
# Set the dimensions for the generator and discriminator
input_dim = 1  # Dimension of the noise input to the generator
output_dim = 1  # Dimension of the generated output (same as real data)

# Create the generator and discriminator
generator = Generator(input_dim=output_dim, output_dim=output_dim)
discriminator = Discriminator(input_dim=output_dim)

# Create the GAN model
gan = GAN(generator, discriminator)

# Train the GAN
gan.train(real_data, epochs=1000, batch_size=32)
# Generate new data after training
num_samples_to_generate = 1000
z = np.random.randn(input_dim, num_samples_to_generate)
generated_data = generator.forward(z)

# Plot real vs generated data
plt.hist(real_data, bins=30, alpha=0.5, label='Real Data')
plt.hist(generated_data, bins=30, alpha=0.5, label='Generated Data')
plt.legend()
plt.title('Real vs Generated Data')
plt.show()
