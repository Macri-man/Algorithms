from PIL import Image, ImageDraw
import math

# Function to generate the L-system string
def generate_l_system(axiom, rules, iterations):
    current = axiom
    for _ in range(iterations):
        next_string = ""
        for char in current:
            next_string += rules.get(char, char)
        current = next_string
    return current

# Function to draw the L-system on an image
def draw_l_system(instructions, angle, length, img_size):
    img = Image.new("RGB", img_size, "white")
    draw = ImageDraw.Draw(img)

    # Starting position and direction
    x, y = img_size[0] // 2, img_size[1]
    stack = []
    direction = 90  # Facing "up"

    # Function to move forward
    def move_forward(length):
        nonlocal x, y
        new_x = x + length * math.cos(math.radians(direction))
        new_y = y - length * math.sin(math.radians(direction))
        draw.line((x, y, new_x, new_y), fill="red", width=1)
        x, y = new_x, new_y

    for command in instructions:
        if command == 'F':
            move_forward(length)
        elif command == '+':
            direction += angle
        elif command == '-':
            direction -= angle
        elif command == '[':
            stack.append((x, y, direction))
        elif command == ']':
            x, y, direction = stack.pop()

    return img

# Main function to set up the L-system parameters and create the image
def main():
    # L-system parameters
    axiom = "F"
    rules = {
        "F": "FF+[+F-F-F]-[-F+F+F]",  # Rule for fractal tree
    }
    
    iterations = 15  # Change for more complexity
    angle = 35      # Turning angle
    length = 8      # Length of each segment
    img_size = (800, 800)  # Image size

    # Generate the L-system instructions
    instructions = generate_l_system(axiom, rules, iterations)
    print("L-system instructions:", instructions)

    # Draw the L-system on an image
    img = draw_l_system(instructions, angle, length, img_size)

    # Save the image to a file
    img.save("fractal_tree.png")
    print("L-System image saved as fractal_tree.png")

if __name__ == "__main__":
    main()
