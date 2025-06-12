import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft2, ifft2, fftshift, ifftshift

# Function to generate a simple color gradient image
def generate_gradient_image(width, height, start_color, end_color):
    """
    Creates a gradient image from start_color to end_color.
    start_color and end_color are RGB tuples.
    """
    r = np.linspace(start_color[0], end_color[0], width).reshape(1, -1)
    g = np.linspace(start_color[1], end_color[1], width).reshape(1, -1)
    b = np.linspace(start_color[2], end_color[2], width).reshape(1, -1)

    gradient = np.zeros((height, width, 3))
    gradient[:, :, 0] = r  # Red channel
    gradient[:, :, 1] = g  # Green channel
    gradient[:, :, 2] = b  # Blue channel
    return gradient / 255.0  # Normalize to [0, 1]

# Generate two gradient images
image1 = generate_gradient_image(256, 256, (255, 255, 255), (0, 0, 255))  
image2 = generate_gradient_image(256, 256, (0, 0, 0), (255, 255, 255))  

# Fourier Transform of the images
def fourier_transform_image(image):
    """Applies Fourier Transform to each channel of an image."""
    channels = [fft2(image[:, :, i]) for i in range(3)]
    return np.stack(channels, axis=-1)

# Inverse Fourier Transform to reconstruct an image
def inverse_fourier_transform_image(f_image):
    """Applies Inverse Fourier Transform to each channel of an image."""
    channels = [ifft2(f_image[:, :, i]).real for i in range(3)]
    return np.stack(channels, axis=-1)

# Apply Fourier Transform
f_image1 = fourier_transform_image(image1)
f_image2 = fourier_transform_image(image2)

# Blend images in the frequency domain
# Example: Mix the magnitude of one and the phase of the other
def blend_images(f_image1, f_image2, alpha=0.5):
    """Blends two Fourier-transformed images."""
    magnitude1 = np.abs(f_image1)
    magnitude2 = np.abs(f_image2)
    phase1 = np.angle(f_image1)
    phase2 = np.angle(f_image2)

    # Blend magnitudes and phases
    blended_magnitude = alpha * magnitude1 + (1 - alpha) * magnitude2
    blended_phase = alpha * phase1 + (1 - alpha) * phase2

    # Reconstruct Fourier-transformed image
    blended = blended_magnitude * np.exp(1j * blended_phase)
    return blended

# Blend the two images
blended_f_image = blend_images(f_image1, f_image2, alpha=0.6)

# Reconstruct the blended image
blended_image = inverse_fourier_transform_image(blended_f_image)

# Normalize the blended image to the [0, 1] range for display
blended_image = np.clip(blended_image, 0, 1)

# Plot the images
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.title("Image 1")
plt.imshow(image1)
plt.axis("off")

plt.subplot(1, 3, 2)
plt.title("Image 2")
plt.imshow(image2)
plt.axis("off")

plt.subplot(1, 3, 3)
plt.title("Blended Image")
plt.imshow(blended_image)
plt.axis("off")

plt.show()
