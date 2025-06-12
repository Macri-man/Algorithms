import random
import math
import numpy as np
import matplotlib.pyplot as plt

# Constants
WIDTH = 50
HEIGHT = 20
NUM_BOIDS = 10
MAX_SPEED = 1
MAX_FORCE = 0.05
SENSE_RADIUS = 5
ALIGN_RADIUS = 3
SEPARATION_RADIUS = 2

# Boid class to represent each individual boid
class Boid:
    def __init__(self, x, y):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.random.rand(2) * 2 - 1  # Random initial velocity
        self.acceleration = np.zeros(2)
        
    def update(self):
        # Update velocity and position
        self.velocity += self.acceleration
        self.velocity = self.limit(self.velocity, MAX_SPEED)
        self.position += self.velocity
        self.acceleration = np.zeros(2)
        
        # Check for NaN values in position and velocity
        if np.isnan(self.position[0]) or np.isnan(self.position[1]):
            print(f"Invalid position detected: {self.position}")
            self.position = np.random.rand(2) * [WIDTH, HEIGHT]  # Reset position randomly
        
        if np.isnan(self.velocity[0]) or np.isnan(self.velocity[1]):
            print(f"Invalid velocity detected: {self.velocity}")
            self.velocity = np.random.rand(2) * 2 - 1  # Reset velocity randomly
        
        # Wrap around if the boid goes out of bounds
        self.position[0] = self.position[0] % WIDTH
        self.position[1] = self.position[1] % HEIGHT
        
    def apply_force(self, force):
        self.acceleration += force
        
    def limit(self, v, max_val):
        # Limit the speed
        magnitude = np.linalg.norm(v)
        if magnitude > max_val:
            return v / magnitude * max_val
        return v
    
    def steer_towards(self, target):
        desired = target - self.position
        desired = self.limit(desired, MAX_SPEED)
        steering = desired - self.velocity
        steering = self.limit(steering, MAX_FORCE)
        return steering
    
    def align(self, boids):
        steering = np.zeros(2)
        total = 0
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < ALIGN_RADIUS:
                steering += boid.velocity
                total += 1
        if total > 0:
            steering /= total
            steering = self.limit(steering, MAX_FORCE)
        return steering
    
    def cohesion(self, boids):
        steering = np.zeros(2)
        total = 0
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < SENSE_RADIUS:
                steering += boid.position
                total += 1
        if total > 0:
            steering /= total
            steering = self.steer_towards(steering)
        return steering
    
    def separation(self, boids):
        steering = np.zeros(2)
        total = 0
        for boid in boids:
            distance = np.linalg.norm(boid.position - self.position)
            if distance < SEPARATION_RADIUS:
                diff = self.position - boid.position
                diff /= distance  # Weight by distance
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            steering = self.limit(steering, MAX_FORCE)
        return steering

# Main simulation for graphical visualization
def simulate_boids():
    boids = [Boid(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)) for _ in range(NUM_BOIDS)]
    boid_positions = []

    for _ in range(100):  # Simulation steps
        for boid in boids:
            alignment = boid.align(boids)
            cohesion = boid.cohesion(boids)
            separation = boid.separation(boids)
            
            boid.apply_force(alignment)
            boid.apply_force(cohesion)
            boid.apply_force(separation)
            boid.update()
        
        boid_positions.append([boid.position.copy() for boid in boids])

    # Visualization using matplotlib
    boid_positions = np.array(boid_positions)
    plt.figure(figsize=(8, 6))
    plt.xlim(0, WIDTH)
    plt.ylim(0, HEIGHT)
    plt.title('Boids Simulation')
    
    for i in range(NUM_BOIDS):
        plt.plot(boid_positions[:, i, 0], boid_positions[:, i, 1], label=f'Boid {i}')
        
    plt.legend()
    plt.show()

# ASCII Visualization for Terminal Output
def print_ascii_boids(boids):
    grid = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for boid in boids:
        x, y = int(boid.position[0]), int(boid.position[1])
        grid[y][x] = '@'
    
    for row in grid:
        print(''.join(row))

# Main simulation for ASCII visualization
def simulate_boids_ascii():
    boids = [Boid(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)) for _ in range(NUM_BOIDS)]
    
    for _ in range(100):  # Simulation steps
        for boid in boids:
            alignment = boid.align(boids)
            cohesion = boid.cohesion(boids)
            separation = boid.separation(boids)
            
            boid.apply_force(alignment)
            boid.apply_force(cohesion)
            boid.apply_force(separation)
            boid.update()
        
        print_ascii_boids(boids)
        print("\n" + "="*WIDTH + "\n")

# Choose which simulation to run
if __name__ == "__main__":
    print("Running Boids Simulation with ASCII visualization...")
    simulate_boids_ascii()  # Uncomment this line for ASCII output in terminal

    print("\nRunning Boids Simulation with Graphical visualization...")
    simulate_boids()  # Uncomment this line for graphical output using matplotlib
