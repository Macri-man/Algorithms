from PIL import Image, ImageDraw
import math

# Function to generate the L-system string
def generate_l_system(axiom, rules, iterations):
    current = axiom
    for _ in range(iterations):
        next_string = ""
        for char in current:
            next_string += rules.get(char, char)
            #print("Char " + char + " " + "String " + rules.get(char, char))
        current = next_string
    return current

# Function to draw the L-system on an image with color-changing rules
def draw_l_system(instructions, angle, length, img_size, start_pos, direction):
    img = Image.new("RGB", img_size, "white")
    draw = ImageDraw.Draw(img)

    # Starting position and direction
    x, y = start_pos  # Custom starting position
    stack = []
    direction = direction  # Facing "up"

    # Default color (black)
    current_color = (0, 0, 0)

    # Function to move forward
    def move_forward(length,draw_line=True):
        nonlocal x, y
        new_x = x + length * math.cos(math.radians(direction))
        new_y = y - length * math.sin(math.radians(direction))
        if draw_line:
            draw.line((x, y, new_x, new_y), fill=current_color, width=1)
        x, y = new_x, new_y

    for command in instructions:
        if command in ('F','X'):
            move_forward(length)
        elif command in ('V','T'):
            move_forward(length, draw_line=False)
        elif command == '+':
            direction += angle
        elif command == '-':
            direction -= angle
        elif command == '[':
            stack.append((x, y, direction, current_color))
        elif command == ']':
            x, y, direction, current_color = stack.pop()

        # Handle color-changing commands
        elif command == 'R':  # Change to red
            current_color = (255, 0, 0)
        elif command == 'G':  # Change to green
            current_color = (0, 255, 0)
        elif command == 'B':  # Change to blue
            current_color = (0, 0, 255)

    return img

# Main function to set up the L-system parameters and create the image
def main():

    #iterations = 5  # Change for more complexity
    #angle = 120      # Turning angle
    #length = 10    # Length of each segment
    length = 10
    img_size = (800, 800)  # Image size


    # L-system parameters

    # Fractal Plant with Colors
    axiom = "F"
    rules = {
        #"F": "F+R[-FGBF]+G[+BFF-F]",  # Rule for fractal tree with color-changing commands
        "F": "FRFB+[+FG-FB-FR]-[-FB+FR+FG]",  # Rule for fractal tree
        "R": "R",  # Color commands pass unchanged
        "G": "G",  # Color commands pass unchanged
        "B": "B",  # Color commands pass unchanged
    }
    iterations = 7
    angle = 35
    direction = 90
    length = 10
    start_pos = (img_size[0]//2 , img_size[1])

    '''
    # Sierpinski Triangle L-system
    axiom = "F"
    rules = {
        "F": "X-F-X",
        "X": "F+X+F"
    }

    iterations = 6
    angle = 60
    direction = 0
    length = 5
    start_pos = (img_size[0]*0 , img_size[1])
    '''
    '''
    # Sierpinski Triangle L-system
    axiom = "F-V-V"
    rules = {
        "F": "F-V+F+V-F",
        "V": "VV"
    }

    iterations = 7
    angle = 120
    direction = 120
    length = 10
    start_pos = (img_size[0]//2 , img_size[1])
    '''
    '''
    # Dragon Curve L-system
    axiom = "FX"
    rules = {
      "X": "X+YF+",
      "Y": "-FX-Y"
    }
    iterations = 10
    angle = 90 
    direction = 90
    length = 10
    start_pos = (img_size[0]//2 , img_size[1]//2)
    '''
    '''
    # Koch Snowflake L-system
    axiom = "F"
    rules = {
      "F": "F+F--F+F"
    }
    iterations = 4
    angle = 60
    direction = 90 
    length = 10
    start_pos = (img_size[0]//2 , img_size[1])
    '''
    '''
    # Fractal Plant L-system
    axiom = "X"
    rules = {
      "X": "F-[[X]+X]+F[+FX]-X",
      "F": "FF"
    }
    iterations = 5
    angle = 25
    direction = 90  
    length = 10
    start_pos = (img_size[0]//2 , img_size[1]) 
    ''' 

    #iterations = 5  # Change for more complexity
    #angle = 120      # Turning angle
    #length = 10    # Length of each segment
    img_size = (800, 800)  # Image size

    # Generate the L-system instructions
    instructions = generate_l_system(axiom, rules, iterations)
    print("L-system instructions:", instructions)

    # Draw the L-system on an image
    img = draw_l_system(instructions, angle, length, img_size,start_pos,direction)

    # Save the image to a file
    img.save("fractal.png")
    print("L-System image saved as fractal.png")

if __name__ == "__main__":
    main()
