import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.spatial import Voronoi
import matplotlib.colors as mcolors

class VoronoiAnimation:
    def __init__(self, n_points=50, grid_size=15, frames=300, interval=33, seed=42):
        """Initialize the Voronoi animation with specified parameters."""
        self.n_points = n_points
        self.grid_size = grid_size
        self.frames = frames
        self.interval = interval
        self.seed = seed
        
        # Set random seed for reproducibility
        np.random.seed(self.seed)
        
        # Initialize points and velocities
        self.points = np.random.rand(self.n_points, 2) * self.grid_size
        self.velocities = (np.random.rand(self.n_points, 2) - 0.5) * 0.1  # Random velocities (±0.02 max)
        
        # Define colors for Voronoi regions
        self.colors = list(mcolors.TABLEAU_COLORS.values())
        
        # Set up figure and axis
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.ax.set_xlim(0, self.grid_size)
        self.ax.set_ylim(0, self.grid_size)
        self.ax.set_aspect('equal')
        self.ax.set_title(f'Voronoi Diagram - {self.n_points} Points', fontsize=15)
        
        # Buffer points to ensure closed Voronoi regions
        self.buffer_points = np.array([
            [-1, -1], [-1, self.grid_size + 1], 
            [self.grid_size + 1, -1], [self.grid_size + 1, self.grid_size + 1],
            [self.grid_size / 2, -1], [self.grid_size / 2, self.grid_size + 1],
            [-1, self.grid_size / 2], [self.grid_size + 1, self.grid_size / 2]
        ])

    def plot_voronoi(self):
        """Plot the Voronoi diagram for the current points."""
        self.ax.clear()
        
        # Set limits and title
        self.ax.set_xlim(0, self.grid_size)
        self.ax.set_ylim(0, self.grid_size)
        self.ax.set_title(f'Voronoi Diagram - {self.n_points} Points', fontsize=15)
        
        # Combine points with buffer points
        all_points = np.vstack([self.points, self.buffer_points])
        
        # Compute Voronoi diagram
        vor = Voronoi(all_points)
        
        # Plot points
        self.ax.plot(self.points[:, 0], self.points[:, 1], 'ko', markersize=6)
        
        # Plot Voronoi regions with colors
        for i, region_idx in enumerate(vor.point_region[:self.n_points]):
            region = vor.regions[region_idx]
            if -1 not in region and region:  # -1 indicates a point at infinity
                polygon = [vor.vertices[i] for i in region]
                poly = plt.Polygon(polygon, fill=True, alpha=0.5, 
                                  color=self.colors[i % len(self.colors)])
                self.ax.add_patch(poly)
        
        # Plot Voronoi edges
        for simplex in vor.ridge_vertices:
            if simplex[0] >= 0 and simplex[1] >= 0:
                self.ax.plot(vor.vertices[simplex, 0], vor.vertices[simplex, 1], 'k-', lw=1)
        
        # Add a legend showing the number of points
        self.ax.text(0.5, 0.02, f'Points: {self.n_points}', transform=self.ax.transAxes, 
                     ha='center', va='bottom', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

    def init_animation(self):
        """Initialize the animation."""
        self.plot_voronoi()
        return self.ax,

    def update(self, frame):
        """Update the animation for each frame using Leapfrog integration."""
        # 1. Update positions
        #print(f'Points: {self.points[0]}')  # Print points before updating (self.points)
        #print(f'Velocities: {self.velocities[0]}')  # Print velocities before updating (self.velocities)
        self.points += self.velocities
        
        # 2. Handle boundary collisions
        min_bound, max_bound = 0.1, self.grid_size - 0.1
        for i in range(self.n_points):
            if self.points[i, 0] <= min_bound or self.points[i, 0] >= max_bound:
                self.velocities[i, 0] *= -1
                self.points[i, 0] = np.clip(self.points[i, 0], min_bound, max_bound)
            if self.points[i, 1] <= min_bound or self.points[i, 1] >= max_bound:
                self.velocities[i, 1] *= -1
                self.points[i, 1] = np.clip(self.points[i, 1], min_bound, max_bound)
        
        
        self.plot_voronoi()
        return self.ax,

    def animate(self, save_path='voronoi_animation.mp4'):
        """Create, display, and save the animation."""
        ani = FuncAnimation(self.fig, self.update, frames=self.frames, 
                            init_func=self.init_animation, interval=self.interval, 
                            blit=True)
        # Save animation
        ani.save(save_path, writer='ffmpeg', fps=30)
        plt.tight_layout()
        plt.show()
        return ani

# Create and run the animation
if __name__ == "__main__":
    voronoi_anim = VoronoiAnimation(n_points=50, grid_size=15, frames=300, interval=33)
    voronoi_anim.animate(save_path='voronoi_animation.mp4')