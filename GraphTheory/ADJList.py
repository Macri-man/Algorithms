from PIL import Image, ImageDraw
import math


class Graph:
    def __init__(self, directed=False):
        self.adj_list = {}
        self.directed = directed

    def add_edge(self, u, v):
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list and not self.directed:
            self.adj_list[v] = []
        
        self.adj_list[u].append(v)
        if not self.directed:
            self.adj_list[v].append(u)

    def display(self):
        for node, neighbors in self.adj_list.items():
            print(f"{node}: {neighbors}")

    def visualize(self, image_size=500):
        img = Image.new("RGB", (image_size, image_size), "white")
        draw = ImageDraw.Draw(img)

        # Compute circular layout
        nodes = list(self.adj_list.keys())
        radius = image_size // 2 - 50
        center = image_size // 2
        angle_step = 2 * math.pi / len(nodes)
        positions = {}

        for i, node in enumerate(nodes):
            angle = i * angle_step
            x = int(center + radius * math.cos(angle))
            y = int(center + radius * math.sin(angle))
            positions[node] = (x, y)

        # Draw edges
        for u in self.adj_list:
            for v in self.adj_list[u]:
                if self.directed or (u < v):  # Avoid drawing duplicates for undirected graphs
                    draw.line([positions[u], positions[v]], fill="gray", width=2)

        # Draw nodes
        for node, (x, y) in positions.items():
            r = 20
            draw.ellipse((x - r, y - r, x + r, y + r), fill="skyblue", outline="black")
            draw.text((x - 6, y - 8), str(node), fill="black")

        img.show()  # This will open the image in the default viewer
        img.save("graph.png")  # Save if needed


def main():
    g = Graph(directed=False)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)
    g.display()
    g.visualize()


if __name__ == "__main__":
    main()
