import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft2, ifft2, fftshift, ifftshift

# Generate a test image with more detail
def generate_test_image(size):
    """Creates a 2D checkerboard pattern for testing."""
    x = np.arange(size)
    y = np.arange(size)
    xv, yv = np.meshgrid(x, y)
    checkerboard = ((xv // 16) % 2) ^ ((yv // 16) % 2)  # Create alternating 16x16 blocks
    return checkerboard.astype(float)

# Create a test image
image = generate_test_image(256)

# Fourier Transform and shift
f_transform = fft2(image)
f_shift = fftshift(f_transform)  # Shift zero frequency to the center for better visualization

# Create a low-pass mask
def create_circular_mask(shape, cutoff_radius):
    """Generates a circular low-pass filter mask."""
    rows, cols = shape
    center_row, center_col = rows // 2, cols // 2
    y, x = np.ogrid[:rows, :cols]
    distance_from_center = np.sqrt((x - center_col)**2 + (y - center_row)**2)
    mask = distance_from_center <= cutoff_radius
    return mask

# Apply the low-pass filter
cutoff_radius = 40
low_pass_mask = create_circular_mask(image.shape, cutoff_radius)

# Apply the mask to the frequency spectrum
f_shift_masked = f_shift * low_pass_mask

# Inverse Fourier Transform
f_ishift = ifftshift(f_shift_masked)  # Reverse the shift
reconstructed_image = np.abs(ifft2(f_ishift))  # Back to spatial domain

# Plot results
plt.figure(figsize=(14, 8))

# Original Image
plt.subplot(2, 3, 1)
plt.title("Original Image")
plt.imshow(image, cmap="gray")
plt.colorbar()
plt.axis("off")

# Fourier Spectrum (Log-scaled for visualization)
plt.subplot(2, 3, 2)
plt.title("Fourier Spectrum (Log Scale)")
plt.imshow(np.log1p(np.abs(f_shift)), cmap="gray")
plt.colorbar()
plt.axis("off")

# Low-pass Mask
plt.subplot(2, 3, 3)
plt.title("Low-pass Mask")
plt.imshow(low_pass_mask, cmap="gray")
plt.colorbar()
plt.axis("off")

# Masked Spectrum
plt.subplot(2, 3, 5)
plt.title("Masked Spectrum")
plt.imshow(np.log1p(np.abs(f_shift_masked)), cmap="gray")
plt.colorbar()
plt.axis("off")

# Reconstructed Image
plt.subplot(2, 3, 6)
plt.title("Reconstructed Image (Low-pass)")
plt.imshow(reconstructed_image, cmap="gray")
plt.colorbar()
plt.axis("off")

plt.tight_layout()
plt.show()
