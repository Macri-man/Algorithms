package main

import (
	"image"
	"image/color"
	"image/png"
	"math/cmplx"
	"os"
)

// Mandelbrot function returns the number of iterations before a point escapes
func mandelbrot(c complex128, maxIter int) int {
	var z complex128
	for n := 0; n < maxIter; n++ {
		if cmplx.Abs(z) > 2 {
			return n
		}
		z = z*z + c
	}
	return maxIter
}

// Generate Mandelbrot set and save as PNG image
func generateMandelbrot(width, height, maxIter int, xmin, xmax, ymin, ymax float64, filename string) {
	img := image.NewRGBA(image.Rect(0, 0, width, height))

	for px := 0; px < width; px++ {
		for py := 0; py < height; py++ {
			x := float64(px)/float64(width)*(xmax-xmin) + xmin
			y := float64(py)/float64(height)*(ymax-ymin) + ymin
			c := complex(x, y)

			// Color based on the number of iterations
			m := mandelbrot(c, maxIter)
			colorVal := uint8(255 - (m * 255 / maxIter))
			col := color.RGBA{colorVal, colorVal, 255 - colorVal, 255}
			img.Set(px, py, col)
		}
	}

	// Save to file
	f, _ := os.Create(filename)
	defer f.Close()
	png.Encode(f, img)
}

func main() {
	// Image parameters
	width, height := 800, 800
	maxIter := 256
	xmin, xmax := -2.5, 1.5
	ymin, ymax := -2.0, 2.0

	// Generate and save the Mandelbrot set
	generateMandelbrot(width, height, maxIter, xmin, xmax, ymin, ymax, "mandelbrot.png")
}
