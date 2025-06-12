import numpy as np
import matplotlib.pyplot as plt

# Mandelbrot Set function
def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n

# Function to generate Mandelbrot fractal
def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    fractal = np.empty((width, height))

    for i in range(width):
        for j in range(height):
            c = complex(r1[i], r2[j])
            fractal[i, j] = mandelbrot(c, max_iter)
    
    return fractal

# Parameters for fractal generation
xmin, xmax, ymin, ymax = -2.5, 1.5, -2.0, 2.0
width, height = 800, 800
max_iter = 256

# Generate the Mandelbrot fractal
fractal = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)

# Plot the result using Matplotlib
plt.imshow(fractal.T, cmap='hot', extent=[xmin, xmax, ymin, ymax])
plt.colorbar()
plt.title("Mandelbrot Set")
plt.show()
