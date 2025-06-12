import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the Lotka-Volterra equations
def lotka_volterra(state, t, alpha, beta, delta, gamma):
    X, Y = state  # Unpack the current state
    dXdt = alpha * X - beta * X * Y
    dYdt = delta * X * Y - gamma * Y
    return [dXdt, dYdt]

# Parameters
alpha = 1.0   # Growth rate of prey
beta = 0.1    # Predation rate coefficient
delta = 0.075 # Rate predators increase by consuming prey
gamma = 1.5   # Death rate of predators

# Initial conditions: [Prey, Predator]
initial_state = [40, 9]

# Time vector
t = np.linspace(0, 200, 1000)

# Integrate the equations over time t.
solution = odeint(lotka_volterra, initial_state, t, args=(alpha, beta, delta, gamma))
prey, predators = solution.T

# Plot population over time
plt.figure(figsize=(12, 5))
plt.plot(t, prey, label="Prey Population", color="blue")
plt.plot(t, predators, label="Predator Population", color="red")
plt.title("Predator and Prey Populations Over Time")
plt.xlabel("Time")
plt.ylabel("Population")
plt.legend()
plt.grid(True)
plt.show()

# Create a phase-space plot (Prey vs Predator) animation
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, max(prey)*1.1)
ax.set_ylim(0, max(predators)*1.1)
ax.set_xlabel("Prey Population")
ax.set_ylabel("Predator Population")
ax.set_title("Phase-Space: Predator vs Prey")
line, = ax.plot([], [], lw=2, color="purple")
point, = ax.plot([], [], 'o', color="black")

def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

def animate(i):
    # Plot data up to the current index i
    xdata = prey[:i]
    ydata = predators[:i]
    line.set_data(xdata, ydata)
    point.set_data(prey[i], predators[i])
    return line, point

ani = animation.FuncAnimation(fig, animate, frames=len(t),
                              init_func=init, interval=20, blit=True)

plt.show()
