import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft2, ifft2, fftshift, ifftshift

# Create a custom image with colorful shapes
def create_custom_image(size=(256, 256)):
    """Generates a simple image with geometric shapes and colors."""
    rows, cols = size
    img = np.zeros((rows, cols, 3))

    # Create a red circle in the center
    y, x = np.ogrid[:rows, :cols]
    center = (rows // 2, cols // 2)
    radius = 50
    mask = (x - center[1])**2 + (y - center[0])**2 <= radius**2
    img[mask] = [1, 0, 0]  # Red color

    # Add a blue square in the top left
    square_size = 60
    img[:square_size, :square_size] = [0, 0, 1]  # Blue color

    # Add a green diagonal line
    for i in range(rows):
        img[i, i:i+1] = [0, 1, 0]  # Green line
    
    return img

# Generate a custom image
image = create_custom_image()

# Fourier Transform and mask application
def apply_fourier_mask(image, mask):
    """Applies a Fourier Transform, masks it, and reconstructs the image."""
    transformed_channels = []
    for channel in range(3):  # Process each RGB channel
        f_transform = fft2(image[..., channel])
        f_shift = fftshift(f_transform)  # Center the FFT
        f_shift_masked = f_shift * mask[..., channel]  # Apply the mask
        f_ishift = ifftshift(f_shift_masked)  # Undo the shift
        reconstructed_channel = np.abs(ifft2(f_ishift))  # Inverse FFT
        transformed_channels.append(reconstructed_channel)
    
    # Stack channels back into an RGB image
    return np.stack(transformed_channels, axis=-1)

# Generate a color mask (same as previous code)
def create_color_mask(shape):
    """Creates a circular gradient color mask."""
    rows, cols, _ = shape
    center_row, center_col = rows // 2, cols // 2
    y, x = np.ogrid[:rows, :cols]
    distance_from_center = np.sqrt((x - center_col)**2 + (y - center_row)**2)
    
    # Normalize distance to [0, 1]
    normalized_distance = distance_from_center / distance_from_center.max()
    
    # Create RGB gradient
    r = 1 - normalized_distance  # Red decreases outward
    g = np.abs(0.5 - normalized_distance)  # Green peaks in the middle
    b = normalized_distance  # Blue increases outward
    mask = np.stack([r, g, b], axis=-1)
    return mask

# Apply the Fourier mask to the custom image
mask = create_color_mask(image.shape)
reconstructed_image = apply_fourier_mask(image, mask)

# Plot results
plt.figure(figsize=(14, 8))

# Original Custom Image
plt.subplot(1, 3, 1)
plt.title("Original Custom Image")
plt.imshow(image)
plt.axis("off")

# Color Mask
plt.subplot(1, 3, 2)
plt.title("Color Mask")
plt.imshow(mask)
plt.axis("off")

# Reconstructed Image after Fourier Masking
plt.subplot(1, 3, 3)
plt.title("Reconstructed Image")
plt.imshow(np.clip(reconstructed_image, 0, 1))  # Ensure values are in [0, 1]
plt.axis("off")

plt.tight_layout()
plt.show()
