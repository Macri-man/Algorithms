import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 60)
ax.set_facecolor('skyblue')

# Draw ground
ground = plt.Rectangle((0, 0), 100, 15, color='forestgreen')
ax.add_patch(ground)

# Elements for weather
sun = plt.Circle((80, 50), 5, color='yellow')
clouds = [plt.Circle((i, 50 + np.sin(i)), 3, color='white') for i in range(10, 60, 10)]
raindrops = [plt.Line2D([], [], color='blue', linewidth=1) for _ in range(20)]
snowflakes = [plt.Text(0, 0, '*', color='white', fontsize=12) for _ in range(20)]

# Add sun and clouds
ax.add_patch(sun)
for cloud in clouds:
    ax.add_patch(cloud)
for rain in raindrops:
    ax.add_line(rain)
for snow in snowflakes:
    ax.add_artist(snow)

# Season colors
season_colors = {
    'spring': 'lightgreen',
    'summer': 'forestgreen',
    'autumn': 'orange',
    'winter': 'white'
}
season_names = list(season_colors.keys())

def update(frame):
    # Determine current season
    season_index = (frame // 50) % 4
    season = season_names[season_index]
    ground.set_color(season_colors[season])

    # Move sun in an arc
    sun_center_x = 80 - 60 * np.cos(2 * np.pi * (frame % 100) / 100)
    sun_center_y = 30 + 20 * np.sin(2 * np.pi * (frame % 100) / 100)
    sun.set_center((sun_center_x, sun_center_y))

    # Cloud movement
    for i, cloud in enumerate(clouds):
        new_x = (cloud.center[0] + 0.5) % 100
        cloud.center = (new_x, cloud.center[1])

    # Weather overlay
    weather = ['sunny', 'rainy', 'snowy'][frame % 150 // 50]

    # Toggle visibility
    if weather == 'rainy':
        for drop in raindrops:
            x = random.uniform(0, 100)
            y1 = random.uniform(30, 60)
            y2 = y1 - 5
            drop.set_data([x, x], [y1, y2])
            drop.set_visible(True)
        for flake in snowflakes:
            flake.set_visible(False)
    elif weather == 'snowy':
        for flake in snowflakes:
            flake.set_position((random.uniform(0, 100), random.uniform(30, 60)))
            flake.set_visible(True)
        for drop in raindrops:
            drop.set_visible(False)
    else:
        for drop in raindrops:
            drop.set_visible(False)
        for flake in snowflakes:
            flake.set_visible(False)

    return [sun] + clouds + raindrops + snowflakes

# Animation
ani = animation.FuncAnimation(fig, update, frames=200, interval=100, blit=True)

plt.title("Weather and Seasons Simulation")
plt.tight_layout()
plt.show()
