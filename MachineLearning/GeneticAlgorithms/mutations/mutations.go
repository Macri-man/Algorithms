package main

import (
	"math/rand"
	"time"
)

// BitFlipMutation
func BitFlipMutation(chromosome []int, mutationRate float64) []int {
	for i := 0; i < len(chromosome); i++ {
		if rand.Float64() < mutationRate { // Chance of mutation
			chromosome[i] = 1 - chromosome[i] // Flip the bit
		}
	}
	return chromosome
}

// SwapMutation
func SwapMutation(chromosome []int, mutationRate float64) []int {
	if rand.Float64() < mutationRate {
		i, j := rand.Intn(len(chromosome)), rand.Intn(len(chromosome))
		for i == j { // Ensure i != j
			j = rand.Intn(len(chromosome))
		}
		chromosome[i], chromosome[j] = chromosome[j], chromosome[i] // Swap values
	}
	return chromosome
}

// ScrambleMutation
func ScrambleMutation(chromosome []int, mutationRate float64) []int {
	if rand.Float64() < mutationRate {
		start, end := rand.Intn(len(chromosome)), rand.Intn(len(chromosome))
		if start > end {
			start, end = end, start
		}
		scrambledSublist := append([]int{}, chromosome[start:end]...)
		rand.Shuffle(len(scrambledSublist), func(i, j int) {
			scrambledSublist[i], scrambledSublist[j] = scrambledSublist[j], scrambledSublist[i]
		})
		copy(chromosome[start:end], scrambledSublist)
	}
	return chromosome
}

// InversionMutation
func InversionMutation(chromosome []int, mutationRate float64) []int {
	if rand.Float64() < mutationRate {
		start, end := rand.Intn(len(chromosome)), rand.Intn(len(chromosome))
		if start > end {
			start, end = end, start
		}
		for i, j := start, end-1; i < j; i, j = i+1, j-1 {
			chromosome[i], chromosome[j] = chromosome[j], chromosome[i] // Reverse the selected range
		}
	}
	return chromosome
}

// GaussianMutation
func GaussianMutation(chromosome []float64, mutationRate float64, sigma float64) []float64 {
	for i := 0; i < len(chromosome); i++ {
		if rand.Float64() < mutationRate {
			chromosome[i] += rand.NormFloat64() * sigma // Add Gaussian noise
		}
	}
	return chromosome
}

// UniformMutation
func UniformMutation(chromosome []float64, mutationRate float64, valueRange [2]float64) []float64 {
	for i := 0; i < len(chromosome); i++ {
		if rand.Float64() < mutationRate {
			chromosome[i] = valueRange[0] + rand.Float64()*(valueRange[1]-valueRange[0]) // Random value in range
		}
	}
	return chromosome
}

// NonUniformMutation
func NonUniformMutation(chromosome []float64, mutationRate float64, generation, maxGenerations int, valueRange [2]float64) []float64 {
	for i := 0; i < len(chromosome); i++ {
		if rand.Float64() < mutationRate {
			delta := (valueRange[1] - valueRange[0]) * (1 - float64(generation)/float64(maxGenerations))
			chromosome[i] += rand.Float64()*2*delta - delta // Apply shrinking delta
			// Ensure the gene stays within the value range
			if chromosome[i] < valueRange[0] {
				chromosome[i] = valueRange[0]
			} else if chromosome[i] > valueRange[1] {
				chromosome[i] = valueRange[1]
			}
		}
	}
	return chromosome
}

// BoundaryMutation
func BoundaryMutation(chromosome []float64, mutationRate float64, valueRange [2]float64) []float64 {
	for i := 0; i < len(chromosome); i++ {
		if rand.Float64() < mutationRate {
			if rand.Float64() < 0.5 {
				chromosome[i] = valueRange[0]
			} else {
				chromosome[i] = valueRange[1]
			} // Choose boundary value
		}
	}
	return chromosome
}

// ArithmeticMutation
func ArithmeticMutation(chromosome []float64, mutationRate float64) []float64 {
	for i := 0; i < len(chromosome); i++ {
		if rand.Float64() < mutationRate {
			chromosome[i] += chromosome[i] * (rand.Float64()*0.2 - 0.1) // Adjust by small percentage
		}
	}
	return chromosome
}

// RandomResettingMutation
func RandomResettingMutation(chromosome []float64, mutationRate float64, valueRange [2]float64) []float64 {
	for i := 0; i < len(chromosome); i++ {
		if rand.Float64() < mutationRate {
			chromosome[i] = valueRange[0] + rand.Float64()*(valueRange[1]-valueRange[0]) // Reset to random value
		}
	}
	return chromosome
}

func main() {
	// Example to initialize the random seed and call mutations
	rand.Seed(time.Now().UnixNano())
	chromosome := []int{1, 0, 1, 0, 1, 0}
	mutationRate := 0.1

	// Test mutation functions
	chromosome = BitFlipMutation(chromosome, mutationRate)
	// Add other mutation functions as needed to test

	// Print the mutated chromosome
	for _, gene := range chromosome {
		print(gene, " ")
	}
}
