from PIL import Image, ImageDraw
import heapq

# Grid size
GRID_WIDTH, GRID_HEIGHT = 20, 20
CELL_SIZE = 25

# Cell types
FREE = 0
OBSTACLE = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions for 4-way movement
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Draw the final grid with path
def draw_grid(grid, path, start, goal):
    img = Image.new("RGB", (GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), WHITE)
    draw = ImageDraw.Draw(img)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = WHITE if grid[y][x] == FREE else BLACK
            draw.rectangle(
                [x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE - 1, (y + 1) * CELL_SIZE - 1],
                fill=color
            )

    for (x, y) in path:
        draw.rectangle(
            [x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE - 1, (y + 1) * CELL_SIZE - 1],
            fill=BLUE
        )

    # Start and goal markers
    sx, sy = start
    gx, gy = goal
    draw.rectangle(
        [sx * CELL_SIZE, sy * CELL_SIZE, (sx + 1) * CELL_SIZE - 1, (sy + 1) * CELL_SIZE - 1],
        fill=GREEN
    )
    draw.rectangle(
        [gx * CELL_SIZE, gy * CELL_SIZE, (gx + 1) * CELL_SIZE - 1, (gy + 1) * CELL_SIZE - 1],
        fill=RED
    )

    img.save("dstar_final.png")

# Manhattan distance
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Priority queue
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def push(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def pop(self):
        return heapq.heappop(self.elements)[1]

    def empty(self):
        return not self.elements

# Basic D* path planning (reverse A* logic)
def d_star(grid, start, goal):
    open_list = PriorityQueue()
    open_list.push(goal, 0)

    g = {goal: 0}
    back_pointer = {}

    while not open_list.empty():
        current = open_list.pop()

        if current == start:
            break

        for dx, dy in DIRS:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                if grid[ny][nx] == OBSTACLE:
                    continue

                cost = 1
                if (nx, ny) not in g or g[(nx, ny)] > g[current] + cost:
                    g[(nx, ny)] = g[current] + cost
                    priority = g[(nx, ny)] + heuristic((nx, ny), start)
                    open_list.push((nx, ny), priority)
                    back_pointer[(nx, ny)] = current

    # Reconstruct path
    path = []
    current = start
    while current != goal:
        path.append(current)
        if current not in back_pointer:
            return []  # No path
        current = back_pointer[current]
    path.append(goal)
    return path

# Main
def main():
    # Build map
    grid = [[FREE for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for i in range(5, 15):
        grid[10][i] = OBSTACLE

    start = (2, 2)
    goal = (18, 15)

    path = d_star(grid, start, goal)
    draw_grid(grid, path, start, goal)

main()
