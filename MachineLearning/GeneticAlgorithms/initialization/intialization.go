package main

import (
	"math"
	"math/rand"
)

// Random Initialization
func randomInitialization(popSize, chromLength int) [][]int {
	population := make([][]int, popSize)
	for i := 0; i < popSize; i++ {
		population[i] = make([]int, chromLength)
		for j := 0; j < chromLength; j++ {
			population[i][j] = rand.Intn(2)
		}
	}
	return population
}

// Heuristic-Based Initialization
func heuristicInitialization(popSize int, cities [][]float64) [][]int {
	bestSolution := make([]int, len(cities))
	bestDistance := math.Inf(1)

	// For demonstration purposes, a simple permutation approach is used here
	// In practice, you should implement a more efficient heuristic
	// (e.g., Nearest Neighbor for TSP)
	permutations := generatePermutations(len(cities))
	for _, perm := range permutations {
		distance := 0.0
		for i := 1; i < len(perm); i++ {
			distance += cities[perm[i-1]][perm[i]]
		}
		if distance < bestDistance {
			bestDistance = distance
			copy(bestSolution, perm)
		}
	}

	population := make([][]int, popSize)
	for i := 0; i < popSize; i++ {
		population[i] = append([]int(nil), bestSolution...)
	}
	return population
}

// Helper function for generating permutations (brute-force approach)
func generatePermutations(n int) [][]int {
	permutations := [][]int{}
	var helper func([]int)
	helper = func(arr []int) {
		if len(arr) == 0 {
			perm := make([]int, n)
			copy(perm, arr)
			permutations = append(permutations, perm)
			return
		}
		for i := 0; i < len(arr); i++ {
			helper(append(arr[:i], arr[i+1:]...))
		}
	}
	helper(make([]int, n))
	return permutations
}

// Seeded Initialization
func seededInitialization(popSize, chromLength int, seeds [][]int) [][]int {
	population := append([][]int(nil), seeds...)
	for len(population) < popSize {
		individual := make([]int, chromLength)
		for i := 0; i < chromLength; i++ {
			individual[i] = rand.Intn(2)
		}
		population = append(population, individual)
	}
	return population
}

// Diverse Initialization
func diverseInitialization(popSize, chromLength int) [][]int {
	population := make([][]int, popSize)
	for i := 0; i < popSize; i++ {
		individual := make([]int, chromLength)
		for j := 0; j < chromLength; j++ {
			if rand.Float64() > 0.5 {
				individual[j] = 1
			} else {
				individual[j] = 0
			}
		}
		population[i] = individual
	}
	return population
}

// Constraint-Based Initialization
func constraintInitialization(popSize, weightLimit int, items [][]int) [][]int {
	population := [][]int{}
	for len(population) < popSize {
		individual := make([]int, len(items))
		for i := 0; i < len(items); i++ {
			individual[i] = rand.Intn(2)
		}
		// Check if weight limit is satisfied
		totalWeight := 0
		for i, gene := range individual {
			if gene == 1 {
				totalWeight += items[i][1]
			}
		}
		if totalWeight <= weightLimit {
			population = append(population, individual)
		}
	}
	return population
}

// Cluster-Based Initialization (for simplicity, using random centroids here)
func clusterBasedInitialization(data [][]float64, popSize, chromLength int) [][]int {
	// In practice, you would use a proper clustering library (e.g., k-means)
	// Here, we're just randomly initializing centroids for demonstration purposes
	population := make([][]int, popSize)
	for i := 0; i < popSize; i++ {
		individual := make([]int, chromLength)
		for j := 0; j < chromLength; j++ {
			individual[j] = rand.Intn(2)
		}
		population[i] = individual
	}
	return population
}

// Gradient-Based Initialization (dummy function for example)
func gradientBasedInitialization(popSize int, gradientFn func([]float64) []float64, bounds [][]float64) [][]float64 {
	population := make([][]float64, popSize)
	for i := 0; i < popSize; i++ {
		solution := gradientFn(bounds)
		population[i] = solution
	}
	return population
}

// Hybrid Initialization
func hybridInitialization(popSize, chromLength int, seeds [][]int) [][]int {
	population := [][]int{}
	numRandom := popSize / 2
	numSeeded := popSize - numRandom

	// Random
	for i := 0; i < numRandom; i++ {
		individual := make([]int, chromLength)
		for j := 0; j < chromLength; j++ {
			individual[j] = rand.Intn(2)
		}
		population = append(population, individual)
	}

	// Seeded
	for i := 0; i < numSeeded; i++ {
		population = append(population, seeds[i%len(seeds)])
	}
	return population
}

// Opposition-Based Initialization
func oppositionBasedInitialization(popSize, chromLength int) [][]int {
	population := randomInitialization(popSize/2, chromLength)
	opposites := make([][]int, len(population))
	for i, individual := range population {
		opposite := make([]int, len(individual))
		for j, gene := range individual {
			opposite[j] = 1 - gene
		}
		opposites[i] = opposite
	}
	return append(population, opposites...)
}

// Fitness-Proportional Initialization
func fitnessProportionalInitialization(popSize int, fitnessFn func([]float64) float64, bounds [][]float64) [][]float64 {
	population := [][]float64{}
	for len(population) < popSize {
		candidate := make([]float64, len(bounds))
		for i := 0; i < len(bounds); i++ {
			candidate[i] = rand.Float64()*(bounds[i][1]-bounds[i][0]) + bounds[i][0]
		}
		if rand.Float64() < fitnessFn(candidate) { // Bias by fitness
			population = append(population, candidate)
		}
	}
	return population
}

// Incremental Initialization
func incrementalInitialization(basePopSize, increment, totalGenerations, chromLength int) [][]int {
	population := [][]int{}
	for gen := 0; gen < totalGenerations; gen++ {
		for i := 0; i < basePopSize+increment*gen; i++ {
			individual := make([]int, chromLength)
			for j := 0; j < chromLength; j++ {
				individual[j] = rand.Intn(2)
			}
			population = append(population, individual)
		}
	}
	return population
}
