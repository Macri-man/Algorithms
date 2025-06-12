import numpy as np
import matplotlib.pyplot as plt

# Set image dimensions
width, height = 512, 512

# Generate random noise
noise = np.random.rand(height, width, 3)  # Random values between 0 and 1 for RGB channels

# Display the image using matplotlib
plt.imshow(noise)
plt.axis('off')  # Turn off axis labels
plt.show()
