import math
from PIL import Image, ImageDraw


class LSystem:
    def __init__(self, axiom, rules, iterations):
        self.axiom = axiom
        self.rules = rules
        self.iterations = iterations

    def generate(self):
        current = self.axiom
        for _ in range(self.iterations):
            next_seq = []
            for char in current:
                next_seq.append(self.rules.get(char, char))
            current = ''.join(next_seq)
        return current


class LSystemDrawer:
    def __init__(self, instructions, angle, length, image_size=(800, 800), start_pos="center", start_angle=0):
        self.instructions = instructions
        self.angle = angle
        self.length = length
        self.image_size = image_size

        self.img = Image.new("RGB", image_size, (255, 255, 255))
        self.draw = ImageDraw.Draw(self.img)

        self.x, self.y = self._get_start_position(start_pos)
        self.heading = start_angle
        self.stack = []

        self.current_color = (0, 0, 0)  # default: black

    def _get_start_position(self, pos):
        w, h = self.image_size
        return {
            "center": (w / 2, h / 2),
            "topleft": (0, 0),
            "topright": (w, 0),
            "bottomleft": (0, h),
            "bottomright": (w, h),
            "topmiddle": (w / 2, 0),
            "bottommiddle": (w / 2, h),
            "leftmiddle": (0, h / 2),
            "rightmiddle": (w, h / 2),
        }.get(pos.lower(), (w / 2, h / 2))

    def draw_lsystem(self):
        for cmd in self.instructions:
            if cmd in ['F','C']:
                new_x = self.x + self.length * math.cos(math.radians(self.heading))
                new_y = self.y - self.length * math.sin(math.radians(self.heading))
                self.draw.line([(self.x, self.y), (new_x, new_y)], fill=self.current_color)
                self.x, self.y = new_x, new_y
            elif cmd == '+':
                self.heading -= self.angle
            elif cmd == '-':
                self.heading += self.angle
            elif cmd == '[':
                self.stack.append((self.x, self.y, self.heading, self.current_color))
            elif cmd == ']':
                self.x, self.y, self.heading, self.current_color = self.stack.pop()
            elif cmd == 'R':
                self.current_color = (255, 0, 0)
            elif cmd == 'G':
                self.current_color = (0, 128, 0)
            elif cmd == 'B':
                self.current_color = (0, 0, 255)

    def save(self, filename):
        self.img.save(filename)
        print(f"Saved: {filename}")


def main():
    axiom = "F"
    rules = {
        "F": "F[+RF]F[-GF]BF"  
    }
    iterations = 6
    angle = 30
    length = 10
    image_size = (800, 800)
    start_pos = "bottommiddle"
    start_angle = 90
    filename = "fractal_tree_colors.png"

    lsystem = LSystem(axiom, rules, iterations)
    instructions = lsystem.generate()

    drawer = LSystemDrawer(
        instructions=instructions,
        angle=angle,
        length=length,
        image_size=image_size,
        start_pos=start_pos,
        start_angle=start_angle
    )
    drawer.draw_lsystem()
    drawer.save(filename)

    # Koch Curve Example
    axiom = "F"
    rules = {
        "F": "FF-[-GF+BF+GF]+[+BF-GF-RF]"
    }
    iterations = 4
    angle = 25
    length = 10
    image_size = (800, 800)
    start_pos = "bottommiddle"
    start_angle = 90

    system = LSystem(axiom, rules, iterations)
    instructions = system.generate()

    drawer = LSystemDrawer(
        instructions=instructions,
        angle=angle,
        length=length,
        image_size=image_size,
        start_pos=start_pos,
        start_angle=start_angle
    )
    drawer.draw_lsystem()
    drawer.save("fractal_tree_colors2.png")


if __name__ == "__main__":
    main()
