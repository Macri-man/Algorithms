import numpy as np
import matplotlib.pyplot as plt

def add_gaussian_noise(image, mean=0, std=25):
    """Add Gaussian noise to an image."""
    # Generate Gaussian noise with the specified mean and standard deviation
    noise = np.random.normal(mean, std, image.shape)
    
    # Add the noise to the image and clip values to stay within the valid range [0, 255]
    noisy_image = np.clip(image + noise, 0, 255)
    
    # Return the noisy image as an unsigned 8-bit integer array
    return noisy_image.astype(np.uint8)

def plot_images(original_image, noisy_image):
    """Display the original and noisy images side by side."""
    # Set up the figure and axes
    plt.figure(figsize=(10, 5))
    
    # Plot the original image
    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(original_image, cmap='gray')
    plt.axis('off')  # Hide the axis for a cleaner look

    # Plot the noisy image
    plt.subplot(1, 2, 2)
    plt.title("Image with Gaussian Noise")
    plt.imshow(noisy_image, cmap='gray')
    plt.axis('off')  # Hide the axis for a cleaner look

    # Show the images
    plt.show()

def main():
    """Main function to generate a simple image, add noise, and display results."""
    # Create a simple gradient image (for example, a 256x256 gradient)
    original_image = np.linspace(0, 255, 256)  # Create a 1D gradient
    original_image = np.tile(original_image, (256, 1))  # Create a 2D gradient by repeating
    
    # Add Gaussian noise to the image
    noisy_image = add_gaussian_noise(original_image)
    
    # Plot the original and noisy images
    plot_images(original_image, noisy_image)

# Run the main function
if __name__ == "__main__":
    main()
