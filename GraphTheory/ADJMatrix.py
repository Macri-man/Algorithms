from PIL import Image, ImageDraw
import math


class Graph:
    def __init__(self, size, directed=False):
        self.size = size
        self.directed = directed
        self.adj_matrix = [[0] * size for _ in range(size)]

    def add_edge(self, u, v):
        self.adj_matrix[u][v] = 1
        if not self.directed:
            self.adj_matrix[v][u] = 1

    def display(self):
        for row in self.adj_matrix:
            print(" ".join(map(str, row)))

    def _draw_arrow(self, draw, start, end, arrow_size=10):
        # Draw line
        draw.line([start, end], fill="gray", width=2)

        # Compute arrowhead points
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)

        # Arrowhead shape
        x3 = end[0] - arrow_size * cos_a
        y3 = end[1] - arrow_size * sin_a

        left = (x3 + arrow_size * math.sin(angle + math.pi / 6),
                y3 - arrow_size * math.cos(angle + math.pi / 6))
        right = (x3 + arrow_size * math.sin(angle - math.pi / 6),
                 y3 - arrow_size * math.cos(angle - math.pi / 6))

        draw.polygon([end, left, right], fill="black")

    def visualize(self, image_size=500):
        img = Image.new("RGB", (image_size, image_size), "white")
        draw = ImageDraw.Draw(img)

        # Circular layout
        radius = image_size // 2 - 50
        center = image_size // 2
        angle_step = 2 * math.pi / self.size
        positions = []

        for i in range(self.size):
            angle = i * angle_step
            x = int(center + radius * math.cos(angle))
            y = int(center + radius * math.sin(angle))
            positions.append((x, y))

        # Draw edges
        for i in range(self.size):
            for j in range(self.size):
                if self.adj_matrix[i][j]:
                    if self.directed:
                        self._draw_arrow(draw, positions[i], positions[j])
                    elif i < j:
                        draw.line([positions[i], positions[j]], fill="gray", width=2)

        # Draw nodes
        for idx, (x, y) in enumerate(positions):
            r = 20
            draw.ellipse((x - r, y - r, x + r, y + r), fill="skyblue", outline="black")
            draw.text((x - 6, y - 8), str(idx), fill="black")

        img.show()
        img.save("graph_matrix_with_arrows.png")


def main():
    g = Graph(5, directed=True)  # Change to True to see arrows
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.display()
    g.visualize()


if __name__ == "__main__":
    main()
