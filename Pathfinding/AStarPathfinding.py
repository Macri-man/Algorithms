from PIL import Image, ImageDraw
import heapq
import random
import imageio.v2 as imageio

# Grid and Cell Size
WIDTH, HEIGHT = 100, 100
CELL_SIZE = 10
VIDEO_PATH = "astar_pathfinding.mp4"

# Generate maze
def generate_maze(width, height, obstacle_chance=0.3):
    grid = [[1 if random.random() > obstacle_chance else 0 for _ in range(width)] for _ in range(height)]
    grid[1][1] = 1
    grid[height - 2][width - 2] = 1
    return grid

# Neighbors
def get_neighbors(pos, width, height):
    x, y = pos
    neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    return [(nx, ny) for nx, ny in neighbors if 0 <= nx < width and 0 <= ny < height]

# Heuristic
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Draw frame
def draw_frame(grid, open_set, closed_set, path, current, frame_list):
    img = Image.new("RGB", (len(grid[0]) * CELL_SIZE, len(grid) * CELL_SIZE), "white")
    draw = ImageDraw.Draw(img)

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            color = "black" if grid[y][x] == 0 else "white"
            draw.rectangle([x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE], fill=color)

    for (x, y) in closed_set:
        draw.rectangle([x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE], fill="lightgray")

    for (x, y) in open_set:
        draw.rectangle([x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE], fill="skyblue")

    if path:
        for (x, y) in path:
            draw.rectangle([x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE], fill="red")

    if current:
        x, y = current
        draw.rectangle([x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE], fill="green")

    frame_list.append(img)

# A* with frame generation
def a_star(grid, start, goal):
    width, height = len(grid[0]), len(grid)
    open_heap = []
    heapq.heappush(open_heap, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    open_set = {start}
    closed_set = set()
    frames = []

    while open_heap:
        _, current = heapq.heappop(open_heap)
        open_set.discard(current)
        closed_set.add(current)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path = path[::-1]
            for _ in range(10):  # hold on final frame
                draw_frame(grid, open_set, closed_set, path, None, frames)
            return path, frames

        for neighbor in get_neighbors(current, width, height):
            if grid[neighbor[1]][neighbor[0]] == 0 or neighbor in closed_set:
                continue

            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                if neighbor not in open_set:
                    heapq.heappush(open_heap, (f_score[neighbor], neighbor))
                    open_set.add(neighbor)

        path = []
        trace = current
        while trace in came_from:
            path.append(trace)
            trace = came_from[trace]
        path.append(start)
        path.reverse()

        draw_frame(grid, open_set, closed_set, path, current, frames)

    return None, frames

# Main
maze = generate_maze(WIDTH, HEIGHT)
start, goal = (1, 1), (WIDTH - 2, HEIGHT - 2)
path, frames = a_star(maze, start, goal)

# Save video
imageio.mimsave(VIDEO_PATH, frames, fps=30)
print(f"{'Path found!' if path else 'No path found.'} Video saved as {VIDEO_PATH}")
