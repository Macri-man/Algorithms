import numpy as np
import matplotlib.pyplot as plt

class ShapeGenerator:
    def __init__(self, r=1):
        self.r = r  # Default radius for shapes
        self.x = None
        self.y = None

    # Function to generate a polygon using a for loop for iteration
    def generate_polygon_iterative(self, n, start_angle=45, angle_unit='degrees'):
        self.x = []
        self.y = []
        # Iterate over the number of sides to calculate each point
        for i in range(n):
            if angle_unit == 'radians':
                theta = start_angle + 2 *np.pi * i/n  # Add start_angle to the angle calculation
                print(f"Theta (in radians) for i={i}: {theta}")
                self.x.append(self.r * np.cos(theta))  # Calculate x-coordinate
                self.y.append(self.r * np.sin(theta))  # Calculate y-coordinate
                print(f"Radians: X coordinates: {self.x}, Y coordinates: {self.y}")
            elif angle_unit == 'degrees':
                theta = start_angle + 360 * i/n
                print(f"Theta (in radians) for i={i}: {theta}")
                self.x.append(self.r * np.cos(np.deg2rad(theta)))  # Calculate x-coordinate 
                self.y.append(self.r * np.sin(np.deg2rad(theta)))  # Calculate y-coordinate
                print(f"Degrees: X coordinates: {self.x}, Y coordinates: {self.y}")
            else:
                print("Invalid angle unit. Use 'radians' or 'degrees'.")    
        # Close the polygon by repeating the first point
        self.x.append(self.x[0])
        self.y.append(self.y[0])


    # Function to generate a circle
    def generate_shape(self, num_points=5):
        theta = np.linspace(0, 2 * np.pi, num_points)
        self.x = self.r * np.cos(theta)
        self.y = self.r * np.sin(theta)

    # Function to plot the shape
    def plot_shape(self):
        if self.x is None or self.y is None:
            raise ValueError("Shape data is not available. Generate a shape first.")
        
        plt.figure(figsize=(6, 6))  # Set figure size
        plt.plot(self.x, self.y, marker='o')  # Plot shape with points
        plt.axis("equal")  # Ensure aspect ratio is equal
        plt.show()  # Show the plot

def main():
    # Create an instance of ShapeGenerator
    shape_generator = ShapeGenerator(r=1)

    # Example 1: Square (4 sides)
    #shape_generator.generate_polygon_iterative(4,45,'degrees')
    #shape_generator.plot_shape()

    # Example 2: Pentagon (5 sides)
    #shape_generator.generate_polygon_iterative(5,18,'degrees')
    #shape_generator.plot_shape()

    # Example 3: Circle (360 points)
    #shape_generator.generate_shape(360)
    #shape_generator.plot_shape()

    # Example 4: Hexagon (6 sides)
    #shape_generator.generate_polygon_iterative(6,30,'degrees')
    #shape_generator.plot_shape()

    # Example 5: Octagon (8 sides)
    #shape_generator.generate_polygon_iterative(8,22.5,'degrees')
    #shape_generator.plot_shape()

    # Example 6: Triangle (3 sides)
    #shape_generator.generate_polygon_iterative(3,60,'degrees')
    #shape_generator.plot_shape()

    # Example 7: Rectangle (4 sides)
    shape_generator.generate_polygon_iterative(4,0,'radians')
    shape_generator.plot_shape()

    # Example 8: Pentagon (5 sides)
    shape_generator.generate_polygon_iterative(5,0,'radians')
    shape_generator.plot_shape()

    # Example 9: Hexagon (6 sides)
    shape_generator.generate_polygon_iterative(6,0,'radians')
    shape_generator.plot_shape()

    # Example 10: Octagon (8 sides)
    shape_generator.generate_polygon_iterative(8,0,'radians')
    shape_generator.plot_shape()


# Call the main function
if __name__ == "__main__":
    main()