import numpy as np
import matplotlib.pyplot as plt

# Generate 2D value noise (simplified Perlin-like noise)
def generate_terrain(width, height, scale=10):
    def interpolate(a0, a1, w):
        return (1.0 - w) * a0 + w * a1

    def smooth_noise(x, y):
        x0 = int(x)
        x1 = x0 + 1
        y0 = int(y)
        y1 = y0 + 1

        sx = x - x0
        sy = y - y0

        n0 = np.random.rand()
        n1 = np.random.rand()
        ix0 = interpolate(n0, n1, sx)

        n2 = np.random.rand()
        n3 = np.random.rand()
        ix1 = interpolate(n2, n3, sx)

        return interpolate(ix0, ix1, sy)

    data = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            nx = x / scale
            ny = y / scale
            data[y][x] = smooth_noise(nx, ny)

    return data

# Parameters
width, height = 100, 100
terrain = generate_terrain(width, height, scale=20)

# Plotting
plt.figure(figsize=(6, 6))
plt.imshow(terrain, cmap='terrain', origin='lower')
plt.colorbar(label='Elevation')
plt.title("Procedurally Generated Terrain")
plt.axis('off')
plt.show()


import numpy as np
import matplotlib.pyplot as plt

# Variation functions
def linear(x, y):
    return x, y

def sinusoidal(x, y):
    return np.sin(x), np.sin(y)

def swirl(x, y):
    r2 = x*x + y*y
    sinr = np.sin(r2)
    cosr = np.cos(r2)
    return x * sinr - y * cosr, x * cosr + y * sinr

# Affine transformations and their variations with weights
transforms = [
    {'a': 0.5, 'b': 0,   'c': 0,   'd': 0.5, 'e': 1,  'f': 0, 'var': linear, 'weight': 0.5},
    {'a': 0.5, 'b': 0,   'c': 0,   'd': 0.5, 'e': -1, 'f': 0, 'var': sinusoidal, 'weight': 0.3},
    {'a': 0.5, 'b': 0,   'c': 0,   'd': 0.5, 'e': 0,  'f': 1, 'var': swirl, 'weight': 0.2},
]

weights = np.array([t['weight'] for t in transforms])
weights /= weights.sum()  # Normalize weights

def apply_transform(x, y, t):
    x_new = t['a'] * x + t['b'] * y + t['e']
    y_new = t['c'] * x + t['d'] * y + t['f']
    return t['var'](x_new, y_new)

# Generate points
num_points = 500000
x, y = 0, 0
points_x = []
points_y = []
colors = []

for i in range(num_points):
    t = np.random.choice(transforms, p=weights)
    x, y = apply_transform(x, y, t)
    if i > 20:  # skip first few to let points settle
        points_x.append(x)
        points_y.append(y)
        colors.append(t['weight'])  # color by transform weight

# Plotting
plt.figure(figsize=(8, 8))
plt.scatter(points_x, points_y, c=colors, s=0.1, cmap='inferno', alpha=0.8)
plt.axis('off')
plt.title("Simplified Flame Fractal Example")
plt.show()


import numpy as np
import matplotlib.pyplot as plt

def rule_30(state):
    """Apply Rule 30 to a 1D binary state array."""
    new_state = np.zeros_like(state)
    for i in range(1, len(state)-1):
        neighborhood = state[i-1]*4 + state[i]*2 + state[i+1]*1
        # Rule 30 in binary: 00011110 (30 decimal)
        # For each neighborhood pattern (0-7), map to output bit:
        rule_30_table = [0,1,1,1,1,0,0,0]
        new_state[i] = rule_30_table[7 - neighborhood]
    return new_state

# Parameters
width = 101       # Number of cells in one row
steps = 50        # Number of time steps

# Initialize the automaton with a single 1 in the center
state = np.zeros(width, dtype=int)
state[width // 2] = 1

# Store history for visualization
history = np.zeros((steps, width), dtype=int)
history[0] = state

# Run the automaton
for t in range(1, steps):
    state = rule_30(state)
    history[t] = state

# Plot the evolution
plt.figure(figsize=(10, 6))
plt.imshow(history, cmap='binary', interpolation='nearest')
plt.title('1D Cellular Automaton: Rule 30')
plt.xlabel('Cell Index')
plt.ylabel('Time Step')
plt.show()


import numpy as np
import matplotlib.pyplot as plt

# Simple smooth noise generator (using interpolation of random grid points)
def smooth_noise(size, scale=10):
    base = np.random.rand(size // scale + 2, size // scale + 2)

    def interpolate(a0, a1, w):
        return (1 - w) * a0 + w * a1

    noise = np.zeros((size, size))
    for y in range(size):
        for x in range(size):
            gx = x / scale
            gy = y / scale

            x0 = int(gx)
            y0 = int(gy)
            xw = gx - x0
            yw = gy - y0

            v00 = base[y0, x0]
            v10 = base[y0, x0+1]
            v01 = base[y0+1, x0]
            v11 = base[y0+1, x0+1]

            ix0 = interpolate(v00, v10, xw)
            ix1 = interpolate(v01, v11, xw)
            noise[y, x] = interpolate(ix0, ix1, yw)

    return noise

# Parameters
size = 200
scale = 20

# Generate noise
noise = smooth_noise(size, scale)

# Plot the noise
plt.figure(figsize=(6, 6))
plt.imshow(noise, cmap='gray')
plt.title("Procedural Noise Example")
plt.axis('off')
plt.show()


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

def hex_tiling(rows, cols, size):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.axis('off')

    # Calculate horizontal and vertical spacing between hex centers
    w = size * 2
    h = np.sqrt(3) * size

    for row in range(rows):
        for col in range(cols):
            # Offset every other row for tessellation
            x = col * w * 0.75
            y = row * h
            if col % 2 == 1:
                y += h / 2

            hexagon = RegularPolygon(
                (x, y),
                numVertices=6,
                radius=size,
                orientation=np.radians(30),
                facecolor=plt.cm.viridis((row * cols + col) / (rows * cols)),
                edgecolor='k'
            )
            ax.add_patch(hexagon)

    ax.set_xlim(-size, cols * w * 0.75 + size)
    ax.set_ylim(-size, rows * h + size)
    plt.title("Hexagonal Tessellation")
    plt.show()

# Parameters
rows = 10
cols = 10
size = 1

hex_tiling(rows, cols, size)


import numpy as np
import matplotlib.pyplot as plt

# Parameter t
t = np.linspace(0, 2 * np.pi, 1000)

# Parametric equations for Lissajous curve
a = 5
b = 4
delta = np.pi / 2
x = np.sin(a * t + delta)
y = np.sin(b * t)

# Plot
plt.figure(figsize=(6,6))
plt.plot(x, y, color='purple')
plt.title("Lissajous Curve")
plt.axis('equal')
plt.grid(True)
plt.show()


import numpy as np
import matplotlib.pyplot as plt

# Target: points inside a circle of radius 1 centered at (0,0)
def fitness(point):
    x, y = point
    dist = np.sqrt(x**2 + y**2)
    # Fitness is higher the closer the point is to the circle radius 1 (absolute difference)
    return 1.0 - abs(dist - 1)

# Create initial population randomly in square [-1.5, 1.5] x [-1.5, 1.5]
pop_size = 100
population = np.random.uniform(-1.5, 1.5, (pop_size, 2))

def select(pop, fits, num=20):
    # Select top num individuals based on fitness
    idx = np.argsort(fits)[-num:]
    return pop[idx]

def crossover(parent1, parent2):
    # Simple average crossover
    return (parent1 + parent2) / 2

def mutate(individual, mutation_rate=0.1):
    if np.random.rand() < mutation_rate:
        individual += np.random.normal(0, 0.1, size=2)
    return individual

# Evolution parameters
generations = 30
mutation_rate = 0.2
selection_size = 20

plt.figure(figsize=(10, 10))
for gen in range(generations):
    # Evaluate fitness
    fits = np.array([fitness(ind) for ind in population])
    
    # Select parents
    parents = select(population, fits, selection_size)
    
    # Create next generation
    next_gen = []
    while len(next_gen) < pop_size:
        p1, p2 = parents[np.random.choice(selection_size, 2, replace=False)]
        child = crossover(p1, p2)
        child = mutate(child, mutation_rate)
        next_gen.append(child)
    population = np.array(next_gen)
    
    # Plot current population
    plt.clf()
    circle = plt.Circle((0, 0), 1, color='gray', fill=False, linewidth=2, linestyle='dashed')
    plt.gca().add_artist(circle)
    plt.scatter(population[:, 0], population[:, 1], c='blue', alpha=0.6, label='Population')
    plt.title(f"Generation {gen+1}")
    plt.xlim(-1.7, 1.7)
    plt.ylim(-1.7, 1.7)
    plt.gca().set_aspect('equal')
    plt.legend()
    plt.pause(0.3)

plt.show()


import matplotlib.pyplot as plt
import numpy as np

def apply_rules(axiom):
    rules = {
        'F': 'FF+[+F-F-F]-[-F+F+F]'
    }
    return ''.join(rules.get(ch, ch) for ch in axiom)

def generate_lsystem(axiom, iterations):
    current = axiom
    for _ in range(iterations):
        current = apply_rules(current)
    return current

def draw_lsystem(instructions, angle=25, length=5):
    stack = []
    x, y = 0, 0
    current_angle = 90  # Pointing up
    positions = [(x, y)]

    for cmd in instructions:
        if cmd == 'F':
            # Move forward
            rad = np.radians(current_angle)
            x_new = x + length * np.cos(rad)
            y_new = y + length * np.sin(rad)
            plt.plot([x, x_new], [y, y_new], color='green')
            x, y = x_new, y_new
        elif cmd == '+':
            current_angle += angle  # Turn right
        elif cmd == '-':
            current_angle -= angle  # Turn left
        elif cmd == '[':
            # Save state
            stack.append((x, y, current_angle))
        elif cmd == ']':
            # Restore state
            x, y, current_angle = stack.pop()

    plt.axis('equal')
    plt.axis('off')
    plt.show()

# Parameters
axiom = 'F'
iterations = 4
angle = 25

# Generate L-system string
lsys_string = generate_lsystem(axiom, iterations)

# Draw the result
draw_lsystem(lsys_string, angle)


import numpy as np
import matplotlib.pyplot as plt

# Particle class to hold position and velocity
class Particle:
    def __init__(self, pos, vel):
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)

    def update(self, dt, gravity, bounds):
        # Update velocity with gravity
        self.vel[1] -= gravity * dt
        # Update position
        self.pos += self.vel * dt

        # Simple collision with bounds (floor at y=0)
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.vel[1] *= -0.7  # bounce with damping

# Initialize particles randomly above ground
num_particles = 50
particles = [Particle([np.random.uniform(-5, 5), np.random.uniform(5, 15)],
                      [np.random.uniform(-1, 1), np.random.uniform(-1, 1)])
             for _ in range(num_particles)]

gravity = 9.81
dt = 0.05
steps = 100

plt.figure(figsize=(8, 6))
for step in range(steps):
    plt.clf()
    for p in particles:
        p.update(dt, gravity, bounds=[-10, 10, 0, 20])
        plt.plot(p.pos[0], p.pos[1], 'bo')

    plt.xlim(-10, 10)
    plt.ylim(0, 20)
    plt.title(f"Particle Simulation - Step {step+1}")
    plt.pause(0.05)

plt.show()


import numpy as np
import matplotlib.pyplot as plt

# Generate data: values that could come from any data source
n_points = 500
theta = np.linspace(0, 8 * np.pi, n_points)
r = np.linspace(0, 10, n_points)
values = np.sin(5 * theta) * np.cos(3 * r)  # synthetic data pattern

# Convert polar to cartesian
x = r * np.cos(theta)
y = r * np.sin(theta)

plt.figure(figsize=(8,8))
sc = plt.scatter(x, y, c=values, cmap='plasma', s=20, alpha=0.8)
plt.axis('equal')
plt.axis('off')
plt.title('Data-Driven Spiral Art')
plt.colorbar(sc, label='Data Value')
plt.show()


import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.axis('off')

circles = []

def on_click(event):
    if event.inaxes:
        # Add a new circle: (x, y, radius, growth_rate, color)
        circles.append([event.xdata, event.ydata, 0.1, 0.1, np.random.rand(3,)])

def update(frame):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    new_circles = []
    for (x, y, r, g, color) in circles:
        circle = plt.Circle((x, y), r, color=color, alpha=0.5)
        ax.add_patch(circle)
        r_new = r + g
        if r_new < 3:
            new_circles.append([x, y, r_new, g, color])
    circles[:] = new_circles

ani = plt.FuncAnimation(fig, update, interval=50)
fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()


import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.axis('off')

circles = []

def on_click(event):
    if event.inaxes:
        # Add a new circle: (x, y, radius, growth_rate, color)
        circles.append([event.xdata, event.ydata, 0.1, 0.1, np.random.rand(3,)])

def update(frame):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    new_circles = []
    for (x, y, r, g, color) in circles:
        circle = plt.Circle((x, y), r, color=color, alpha=0.5)
        ax.add_patch(circle)
        r_new = r + g
        if r_new < 3:
            new_circles.append([x, y, r_new, g, color])
    circles[:] = new_circles

ani = plt.FuncAnimation(fig, update, interval=50)
fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()
