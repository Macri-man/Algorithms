package main

import (
	"math/rand"
)

// Single-Point Crossover
func singlePointCrossover(parent1, parent2 []int) ([]int, []int) {
	if len(parent1) != len(parent2) {
		panic("Parents must be of the same length")
	}

	point := rand.Intn(len(parent1)-1) + 1

	offspring1 := append(append([]int(nil), parent1[:point]...), parent2[point:]...)
	offspring2 := append(append([]int(nil), parent2[:point]...), parent1[point:]...)

	return offspring1, offspring2
}

// Two-Point Crossover
func twoPointCrossover(parent1, parent2 []int) ([]int, []int) {
	if len(parent1) != len(parent2) {
		panic("Parents must be of the same length")
	}

	point1 := rand.Intn(len(parent1)-2) + 1
	point2 := rand.Intn(len(parent1)-point1-1) + point1 + 1

	offspring1 := append(append([]int(nil), parent1[:point1]...), append(parent2[point1:point2], parent1[point2:]...)...)
	offspring2 := append(append([]int(nil), parent2[:point1]...), append(parent1[point1:point2], parent2[point2:]...)...)

	return offspring1, offspring2
}

// Uniform Crossover
func uniformCrossover(parent1, parent2 []int) ([]int, []int) {
	if len(parent1) != len(parent2) {
		panic("Parents must be of the same length")
	}

	offspring1 := []int{}
	offspring2 := []int{}

	for i := 0; i < len(parent1); i++ {
		if rand.Float64() < 0.5 {
			offspring1 = append(offspring1, parent1[i])
			offspring2 = append(offspring2, parent2[i])
		} else {
			offspring1 = append(offspring1, parent2[i])
			offspring2 = append(offspring2, parent1[i])
		}
	}

	return offspring1, offspring2
}

// Arithmetic Crossover
func arithmeticCrossover(parent1, parent2 []float64, alpha float64) ([]float64, []float64) {
	if len(parent1) != len(parent2) {
		panic("Parents must be of the same length")
	}

	offspring1 := make([]float64, len(parent1))
	offspring2 := make([]float64, len(parent1))

	for i := 0; i < len(parent1); i++ {
		offspring1[i] = alpha*parent1[i] + (1-alpha)*parent2[i]
		offspring2[i] = (1-alpha)*parent1[i] + alpha*parent2[i]
	}

	return offspring1, offspring2
}

// Blend Crossover (BLX-α)
func blendCrossover(parent1, parent2 []float64, alpha float64) ([]float64, []float64) {
	if len(parent1) != len(parent2) {
		panic("Parents must be of the same length")
	}

	offspring1 := []float64{}
	offspring2 := []float64{}

	for i := 0; i < len(parent1); i++ {
		lower := parent1[i] - alpha*abs(parent1[i]-parent2[i])
		upper := parent1[i] + alpha*abs(parent1[i]-parent2[i])

		offspring1 = append(offspring1, rand.Float64()*(upper-lower)+lower)
		offspring2 = append(offspring2, rand.Float64()*(upper-lower)+lower)
	}

	return offspring1, offspring2
}

// Helper function for absolute value
func abs(a float64) float64 {
	if a < 0 {
		return -a
	}
	return a
}

// Partially Matched Crossover (PMX)
func partiallyMatchedCrossover(parent1, parent2 []int) ([]int, []int) {
	if len(parent1) != len(parent2) {
		panic("Parents must be of the same length")
	}

	point1 := rand.Intn(len(parent1) - 1)
	point2 := rand.Intn(len(parent1)-point1-1) + point1 + 1

	offspring1 := append(append([]int(nil), parent1[:point1]...), append(parent2[point1:point2], parent1[point2:]...)...)
	offspring2 := append(append([]int(nil), parent2[:point1]...), append(parent1[point1:point2], parent2[point2:]...)...)

	// Repair offspring to maintain uniqueness
	offspring1 = repairPMX(offspring1, parent1, parent2, point1, point2)
	offspring2 = repairPMX(offspring2, parent2, parent1, point1, point2)

	return offspring1, offspring2
}

func repairPMX(offspring, parent1, parent2 []int, point1, point2 int) []int {
	for i := point1; i < point2; i++ {
		if contains(offspring[:point1], offspring[i]) || contains(offspring[point2:], offspring[i]) {
			// Repair by replacing duplicate genes with the missing ones
			missingGene := findMissingGene(parent1, parent2, offspring)
			offspring[i] = missingGene
		}
	}
	return offspring
}

func contains(slice []int, value int) bool {
	for _, v := range slice {
		if v == value {
			return true
		}
	}
	return false
}

func findMissingGene(parent1, parent2, offspring []int) int {
	geneSet := make(map[int]bool)
	for _, gene := range append(parent1, parent2...) {
		geneSet[gene] = true
	}

	for _, gene := range offspring {
		delete(geneSet, gene)
	}

	for gene := range geneSet {
		return gene
	}
	return -1
}

// Order Crossover (OX)
func orderCrossover(parent1, parent2 []int) ([]int, []int) {
	if len(parent1) != len(parent2) {
		panic("Parents must be of the same length")
	}

	size := len(parent1)
	point1 := rand.Intn(size - 1)
	point2 := rand.Intn(size-point1-1) + point1 + 1

	offspring1 := make([]int, size)
	offspring1[point1:point2] = append([]int(nil), parent1[point1:point2]...)
	offspring2 := make([]int, size)
	offspring2[point1:point2] = append([]int(nil), parent2[point1:point2]...)

	currentIndex := point2
	for _, gene := range parent2 {
		if !contains(offspring1[:point1], gene) && !contains(offspring1[point2:], gene) {
			if currentIndex == size {
				currentIndex = 0
			}
			offspring1[currentIndex] = gene
			currentIndex++
		}
	}

	currentIndex = point2
	for _, gene := range parent1 {
		if !contains(offspring2[:point1], gene) && !contains(offspring2[point2:], gene) {
			if currentIndex == size {
				currentIndex = 0
			}
			offspring2[currentIndex] = gene
			currentIndex++
		}
	}

	return offspring1, offspring2
}

// Cycle Crossover (CX)
func cycleCrossover(parent1, parent2 []int) ([]int, []int) {
	if len(parent1) != len(parent2) {
		panic("Parents must be of the same length")
	}

	size := len(parent1)
	offspring1 := make([]int, size)
	offspring2 := make([]int, size)

	// Start with the first unfilled position in offspring1
	i := 0
	for containsUnfilled(offspring1) {
		current := i
		for offspring1[current] == 0 {
			offspring1[current] = parent1[current]
			offspring2[current] = parent2[current]
			current = findIndex(parent2, parent1[current])
		}
	}

	return offspring1, offspring2
}

func containsUnfilled(slice []int) bool {
	for _, value := range slice {
		if value == 0 {
			return true
		}
	}
	return false
}

func findIndex(slice []int, value int) int {
	for i, v := range slice {
		if v == value {
			return i
		}
	}
	return -1
}
