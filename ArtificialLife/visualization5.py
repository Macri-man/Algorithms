import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Setup
np.random.seed(123)
products = ["Product A", "Product B", "Product C"]
num_products = len(products)
steps = 100
max_capacity = 100
restock_threshold = 20

# Initialize stock histories
inventories = [[50] for _ in products]
x_data = [[] for _ in products]
y_data = [[] for _ in products]

# Create subplots
fig, axes = plt.subplots(1, num_products, figsize=(15, 5), sharey=True)
lines = []

for i, ax in enumerate(axes):
    ax.set_xlim(0, steps)
    ax.set_ylim(0, max_capacity + 10)
    ax.set_title(products[i])
    ax.set_xlabel("Time Step")
    if i == 0:
        ax.set_ylabel("Item Count")
    ax.axhline(restock_threshold, color='red', linestyle='--', label='Restock Threshold')
    line, = ax.plot([], [], lw=2)
    lines.append(line)

# Update function for animation
def update(frame):
    for i in range(num_products):
        current = inventories[i][-1]

        # Purchases and restocks
        purchases = np.random.randint(0, 11)
        current -= purchases
        if current < restock_threshold:
            current += np.random.randint(20, 51)
        current = min(max(current, 0), max_capacity)

        inventories[i].append(current)
        x_data[i].append(frame)
        y_data[i].append(current)
        lines[i].set_data(x_data[i], y_data[i])
    return lines

# Animate
ani = animation.FuncAnimation(fig, update, frames=range(1, steps + 1), blit=True, repeat=False, interval=200)

plt.tight_layout()
plt.show()
