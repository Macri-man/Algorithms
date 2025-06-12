package LSystemConfig

import (
	"image/color"
)

type LSystemConfig struct {
	Axioms       string
	Rules        map[string]string
	Instructions string
	Iterations   int
	Filename     string
	Length       float64
	Angle        float64
	Direction    float64
	Color        color.RGBA
	ImageSize    [2]int
	StartPos     [2]int
}

func NewLSystemConfig(axioms string, rules map[string]string, iterations int, length float64, angle float64, direction float64, startPos string, color color.RGBA, imageSize [2]int, filename string) *LSystemConfig {
	config := &LSystemConfig{
		Axioms:       axioms,
		Rules:        rules,
		Instructions: "",
		Iterations:   iterations,
		Angle:        angle,
	}

	config.Filename = config.defaultFilename(filename)
	config.Length = config.startingLength(length)
	config.Direction = config.startingDirection(direction)
	config.Color = config.startingColor(color)
	config.ImageSize = config.startingImageSize(imageSize)
	config.StartPos = config.startPoint(startPos)

	return config
}

func (c *LSystemConfig) defaultFilename(filename string) string {
	if filename != "" {
		return filename
	}
	return "Fractals.png"
}

func (c *LSystemConfig) startingDirection(direction float64) float64 {
	if direction != 0 {
		return direction
	}
	return 0
}

func (c *LSystemConfig) startingLength(length float64) float64 {
	if length != 0 {
		return length
	}
	return 5
}

func (c *LSystemConfig) startingImageSize(imageSize [2]int) [2]int {
	if imageSize != [2]int{0, 0} {
		return imageSize
	}
	return [2]int{800, 800}
}

func (c *LSystemConfig) startingColor(col color.RGBA) color.RGBA {
	if col != (color.RGBA{}) {
		return col
	}
	return color.RGBA{0, 0, 0, 255}
}

func (c *LSystemConfig) startPoint(pos string) [2]int {
	startingPoints := map[string][2]int{
		"topLeft":      {0, 0},
		"topRight":     {c.ImageSize[0], 0},
		"middle":       {c.ImageSize[0] / 2, c.ImageSize[1] / 2},
		"bottomMiddle": {c.ImageSize[0] / 2, c.ImageSize[1]},
		"topMiddle":    {c.ImageSize[0] / 2, 0},
		"bottomLeft":   {0, c.ImageSize[1]},
		"bottomRight":  {c.ImageSize[0], c.ImageSize[1]},
	}

	if point, ok := startingPoints[pos]; ok {
		return point
	}

	return [2]int{c.ImageSize[0] / 2, c.ImageSize[1]}
}
