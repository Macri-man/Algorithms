package main

import (
	"fmt"
	"image"
	"image/color"
	"image/draw"
	"image/png"
	"math"
	"os"
)

// Function to generate the L-system string
func generateLSystem(axiom string, rules map[string]string, iterations int) string {
	current := axiom
	for i := 0; i < iterations; i++ {
		next := ""
		for _, char := range current {
			if replacement, exists := rules[string(char)]; exists {
				next += replacement
			} else {
				next += string(char)
			}
		}
		current = next
	}
	return current
}

// Function to draw the L-system on the image
func drawLSystem(instructions string, angle float64, img *image.RGBA, scale float64) {
	var stack []State
	x, y := 400.0, 400.0 // Starting position at the center of the image
	direction := 90.0    // Start facing "up"

	// Initial point
	prevX, prevY := x, y

	for _, command := range instructions {
		switch command {
		case 'F':
			// Move forward and store the new point
			prevX, prevY = x, y
			x += math.Cos(direction*math.Pi/180) * scale
			y += math.Sin(direction*math.Pi/180) * scale
			// Draw a line between the points
			drawLine(img, int(prevX), int(prevY), int(x), int(y), color.RGBA{255, 255, 255, 255}) // Blue lines

		case '+':
			// Turn right
			direction += angle

		case '-':
			// Turn left
			direction -= angle

		case '[':
			// Save current state (direction and position)
			stack = append(stack, State{direction, x, y})

		case ']':
			// Restore previous state (direction and position)
			if len(stack) > 0 {
				lastState := stack[len(stack)-1]
				stack = stack[:len(stack)-1]
				direction = lastState.direction
				x, y = lastState.x, lastState.y
			}
		}
	}
}

// State struct to store the direction and position
type State struct {
	direction float64
	x, y      float64
}

// Function to draw a line between two points
func drawLine(img *image.RGBA, x1, y1, x2, y2 int, col color.Color) {
	dx := abs(x2 - x1)
	dy := abs(y2 - y1)

	sx := -1
	if x1 < x2 {
		sx = 1
	}
	sy := -1
	if y1 < y2 {
		sy = 1
	}
	err := dx - dy

	for {
		img.Set(x1, y1, col)

		if x1 == x2 && y1 == y2 {
			break
		}
		e2 := 2 * err
		if e2 > -dy {
			err -= dy
			x1 += sx
		}
		if e2 < dx {
			err += dx
			y1 += sy
		}
	}
}

// Helper function to calculate the absolute value of an integer
func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func main() {
	// L-system parameters for Fractal Tree
	axiom := "F"
	rules := map[string]string{
		"F": "F+F−F−F+F", // Rule for fractal tree
	}
	iterations := 15 // Adjust this for more complex patterns
	angle := 90.0    // Turning angle
	scale := 2.0     // Length of each line segment

	// Generate the L-system instructions
	instructions := generateLSystem(axiom, rules, iterations)
	fmt.Println("L-system instructions:", instructions)

	// Create a blank image
	width, height := 800, 800
	img := image.NewRGBA(image.Rect(0, 0, width, height))

	// Fill the background with white
	draw.Draw(img, img.Bounds(), &image.Uniform{color.White}, image.Point{}, draw.Src)

	// Draw the L-system on the image
	drawLSystem(instructions, angle, img, scale)

	// Save the image to a file
	outputFile, err := os.Create("fractal_tree.png")
	if err != nil {
		fmt.Println("Error creating file:", err)
		return
	}
	defer outputFile.Close()

	// Encode the image as PNG
	png.Encode(outputFile, img)
	fmt.Println("L-System image saved as fractal_tree.png")
}
