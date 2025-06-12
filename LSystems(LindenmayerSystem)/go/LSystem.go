package LSystem

import (
	"fmt"
	"image"
	"image/color"
	"image/png"
	"math"
	"os"
	"regexp"
	"strings"
)

type LSystemConfig struct {
	Axioms     string
	Rules      map[string]string
	Iterations int
	Filename   string
	StartPos   [2]float64
	Angle      float64
	Direction  float64
	ImageSize  [2]int
	Length     float64
	Color      color.Color
}

type LSystem struct {
	config          LSystemConfig
	instructions    string
	image           *image.RGBA
	commandsActions map[string]func()
	stack           [][7]float64
	x, y            float64
	xlen, ylen      float64
}

func NewLSystem(config LSystemConfig) *LSystem {
	ls := &LSystem{
		config:       config,
		instructions: config.Axioms,
		image:        image.NewRGBA(image.Rect(0, 0, config.ImageSize[0], config.ImageSize[1])),
		stack:        make([][7]float64, 0),
		x:            config.StartPos[0],
		y:            config.StartPos[1],
		xlen:         config.Length,
		ylen:         config.Length,
	}
	ls.commandsActions = ls.getCommands()
	return ls
}

func (ls *LSystem) generateLSystemString() {
	for i := 0; i < ls.config.Iterations; i++ {
		var newInstructions strings.Builder
		for _, char := range ls.instructions {
			if replacement, ok := ls.config.Rules[string(char)]; ok {
				newInstructions.WriteString(replacement)
			} else {
				newInstructions.WriteRune(char)
			}
		}
		ls.instructions = newInstructions.String()
	}
}

func (ls *LSystem) simplifyInstructions() {
	re := regexp.MustCompile(`([A-Za-z])\d+`)
	ls.instructions = re.ReplaceAllString(ls.instructions, "$1")
}

func (ls *LSystem) getCommands() map[string]func() {
	return map[string]func(){
		"L": ls.drawLine,
		"C": ls.drawCircle,
		"S": ls.drawSquare,
		"E": ls.drawEllipse,
		"M": ls.moveFocus,
		"N": func() {}, // drawNothing
		"+": func() { ls.updateDirection(ls.config.Angle) },
		"-": func() { ls.updateDirection(-ls.config.Angle) },
		"[": ls.pushStack,
		"]": ls.popStack,
		"R": func() { ls.changeColor(color.RGBA{255, 0, 0, 255}) },
		"G": func() { ls.changeColor(color.RGBA{0, 255, 0, 255}) },
		"B": func() { ls.changeColor(color.RGBA{0, 0, 255, 255}) },
	}
}

func (ls *LSystem) moveFocus() {
	ls.x += ls.config.Length * math.Cos(ls.config.Direction*math.Pi/180)
	ls.y -= ls.config.Length * math.Sin(ls.config.Direction*math.Pi/180)
}

func (ls *LSystem) drawLine() {
	newX := ls.x + ls.config.Length*math.Cos(ls.config.Direction*math.Pi/180)
	newY := ls.y - ls.config.Length*math.Sin(ls.config.Direction*math.Pi/180)
	drawLine(ls.image, int(ls.x), int(ls.y), int(newX), int(newY), ls.config.Color)
	ls.x, ls.y = newX, newY
}

func (ls *LSystem) drawCircle() {
	drawCircle(ls.image, int(ls.x), int(ls.y), int(ls.config.Length), ls.config.Color)
}

func (ls *LSystem) drawSquare() {
	drawRectangle(ls.image, int(ls.x-ls.config.Length/2), int(ls.y-ls.config.Length/2),
		int(ls.x+ls.config.Length/2), int(ls.y+ls.config.Length/2), ls.config.Color)
}

func (ls *LSystem) drawEllipse() {
	drawEllipse(ls.image, int(ls.x-ls.xlen), int(ls.y-ls.ylen),
		int(ls.x+ls.xlen), int(ls.y+ls.ylen), ls.config.Color)
}

func (ls *LSystem) updateDirection(angle float64) {
	ls.config.Direction += angle
}

func (ls *LSystem) pushStack() {
	ls.stack = append(ls.stack, [7]float64{ls.x, ls.y, ls.config.Direction, float64(ls.config.Color.(color.RGBA).R),
		float64(ls.config.Color.(color.RGBA).G), float64(ls.config.Color.(color.RGBA).B), ls.config.Length})
}

func (ls *LSystem) popStack() {
	if len(ls.stack) > 0 {
		last := ls.stack[len(ls.stack)-1]
		ls.stack = ls.stack[:len(ls.stack)-1]
		ls.x, ls.y, ls.config.Direction = last[0], last[1], last[2]
		ls.config.Color = color.RGBA{uint8(last[3]), uint8(last[4]), uint8(last[5]), 255}
		ls.config.Length = last[6]
	}
}

func (ls *LSystem) changeColor(newColor color.Color) {
	ls.config.Color = newColor
}

func (ls *LSystem) executeCommands() {
	for _, command := range ls.instructions {
		if action, ok := ls.commandsActions[string(command)]; ok {
			action()
		} else {
			fmt.Printf("Unknown command: %c\n", command)
		}
	}
}

func (ls *LSystem) save() error {
	f, err := os.Create(ls.config.Filename)
	if err != nil {
		return err
	}
	defer f.Close()
	return png.Encode(f, ls.image)
}

func (ls *LSystem) run() error {
	ls.generateLSystemString()
	fmt.Println("L-system Instructions:", ls.instructions)
	ls.simplifyInstructions()
	fmt.Println("Simplified L-system Instructions:", ls.instructions)
	ls.executeCommands()
	err := ls.save()
	if err != nil {
		return err
	}
	fmt.Println("L-System image saved as", ls.config.Filename)
	return nil
}

// Helper functions for drawing

func drawLine(img *image.RGBA, x1, y1, x2, y2 int, c color.Color) {
	// Bresenham's line algorithm
	dx := abs(x2 - x1)
	dy := abs(y2 - y1)
	sx, sy := 1, 1
	if x1 >= x2 {
		sx = -1
	}
	if y1 >= y2 {
		sy = -1
	}
	err := dx - dy

	for {
		img.Set(x1, y1, c)
		if x1 == x2 && y1 == y2 {
			return
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

func drawCircle(img *image.RGBA, x0, y0, radius int, c color.Color) {
	// Midpoint circle algorithm
	x, y := radius, 0
	dx, dy := 1, 1
	err := dx - (radius * 2)

	for x >= y {
		img.Set(x0+x, y0+y, c)
		img.Set(x0+y, y0+x, c)
		img.Set(x0-y, y0+x, c)
		img.Set(x0-x, y0+y, c)
		img.Set(x0-x, y0-y, c)
		img.Set(x0-y, y0-x, c)
		img.Set(x0+y, y0-x, c)
		img.Set(x0+x, y0-y, c)

		if err <= 0 {
			y++
			err += dy
			dy += 2
		}
		if err > 0 {
			x--
			dx += 2
			err += dx - (radius * 2)
		}
	}
}

func drawRectangle(img *image.RGBA, x1, y1, x2, y2 int, c color.Color) {
	for x := x1; x <= x2; x++ {
		img.Set(x, y1, c)
		img.Set(x, y2, c)
	}
	for y := y1; y <= y2; y++ {
		img.Set(x1, y, c)
		img.Set(x2, y, c)
	}
}

func drawEllipse(img *image.RGBA, x0, y0, x1, y1 int, c color.Color) {
	// Bresenham's ellipse algorithm
	a := abs(x1 - x0)
	b := abs(y1 - y0)
	b1 := b & 1
	dx := 4 * (1 - a) * b * b
	dy := 4 * (b1 + 1) * a * a
	err := dx + dy + b1*a*a

	if x0 > x1 {
		x0 = x1
		x1 += a
	}
	if y0 > y1 {
		y0 = y1
	}
	y0 += (b + 1) / 2
	y1 = y0 - b1
	a *= 8 * a
	b1 = 8 * b * b

	for {
		img.Set(x1, y0, c)
		img.Set(x0, y0, c)
		img.Set(x0, y1, c)
		img.Set(x1, y1, c)
		e2 := 2 * err
		if e2 <= dy {
			y0++
			y1--
			err += dy
			dy += a
		}
		if e2 >= dx || 2*err > dy {
			x0++
			x1--
			err += dx
			dx += b1
		}
		if x0 > x1 {
			break
		}
	}

	for y0-y1 < b {
		img.Set(x0-1, y0, c)
		img.Set(x1+1, y0, c)
		y0++
		img.Set(x0-1, y1, c)
		img.Set(x1+1, y1, c)
		y1--
	}
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}
