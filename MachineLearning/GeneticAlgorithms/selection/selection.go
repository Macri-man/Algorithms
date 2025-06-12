package main

import (
	"math"
	"math/rand"
	"time"
)

// Roulette Wheel Selection
func rouletteWheelSelection(population []interface{}, fitnessValues []float64) interface{} {
	var totalFitness float64
	for _, fitness := range fitnessValues {
		totalFitness += fitness
	}
	probabilities := make([]float64, len(fitnessValues))
	for i, fitness := range fitnessValues {
		probabilities[i] = fitness / totalFitness
	}
	cumulativeProbabilities := make([]float64, len(probabilities))
	cumulativeProbabilities[0] = probabilities[0]
	for i := 1; i < len(probabilities); i++ {
		cumulativeProbabilities[i] = cumulativeProbabilities[i-1] + probabilities[i]
	}

	rand.Seed(time.Now().UnixNano())
	randValue := rand.Float64()

	for i, cumulative := range cumulativeProbabilities {
		if randValue <= cumulative {
			return population[i]
		}
	}
	return nil
}

// Rank-Based Selection
func rankBasedSelection(population []interface{}, fitnessValues []float64) interface{} {
	sortedPopulation := make([]interface{}, len(population))
	copy(sortedPopulation, population)
	ranks := make([]int, len(population))
	for i := range ranks {
		ranks[i] = i + 1
	}
	totalRank := 0
	for _, rank := range ranks {
		totalRank += rank
	}
	probabilities := make([]float64, len(ranks))
	for i, rank := range ranks {
		probabilities[i] = float64(rank) / float64(totalRank)
	}
	cumulativeProbabilities := make([]float64, len(probabilities))
	cumulativeProbabilities[0] = probabilities[0]
	for i := 1; i < len(probabilities); i++ {
		cumulativeProbabilities[i] = cumulativeProbabilities[i-1] + probabilities[i]
	}

	rand.Seed(time.Now().UnixNano())
	randValue := rand.Float64()

	for i, cumulative := range cumulativeProbabilities {
		if randValue <= cumulative {
			return sortedPopulation[i]
		}
	}
	return nil
}

// Tournament Selection
func tournamentSelection(population []interface{}, fitnessValues []float64, tournamentSize int) interface{} {
	rand.Seed(time.Now().UnixNano())
	participants := make([][2]interface{}, tournamentSize)
	for i := 0; i < tournamentSize; i++ {
		participants[i] = [2]interface{}{population[rand.Intn(len(population))], fitnessValues[rand.Intn(len(fitnessValues))]}
	}

	var winner [2]interface{}
	maxFitness := -math.MaxFloat64
	for _, participant := range participants {
		if participant[1].(float64) > maxFitness {
			winner = participant
			maxFitness = participant[1].(float64)
		}
	}

	return winner[0]
}

// Truncation Selection
func truncationSelection(population []interface{}, fitnessValues []float64, proportion float64) interface{} {
	sortedPopulation := make([]interface{}, len(population))
	copy(sortedPopulation, population)

	// Sort the population by fitness values
	for i := 0; i < len(fitnessValues)-1; i++ {
		for j := i + 1; j < len(fitnessValues); j++ {
			if fitnessValues[i] < fitnessValues[j] {
				fitnessValues[i], fitnessValues[j] = fitnessValues[j], fitnessValues[i]
				sortedPopulation[i], sortedPopulation[j] = sortedPopulation[j], sortedPopulation[i]
			}
		}
	}
	cutoff := int(float64(len(population)) * proportion)
	return sortedPopulation[rand.Intn(cutoff)]
}

// Stochastic Universal Sampling (SUS)
func stochasticUniversalSampling(population []interface{}, fitnessValues []float64, numSelected int) []interface{} {
	var totalFitness float64
	for _, fitness := range fitnessValues {
		totalFitness += fitness
	}
	pointDistance := totalFitness / float64(numSelected)
	startPoint := rand.Float64() * pointDistance
	points := make([]float64, numSelected)
	for i := range points {
		points[i] = startPoint + float64(i)*pointDistance
	}

	selected := []interface{}{}
	cumulativeFitness := 0.0
	index := 0
	for _, point := range points {
		for cumulativeFitness < point {
			cumulativeFitness += fitnessValues[index]
			index++
		}
		selected = append(selected, population[index-1])
	}
	return selected
}

// Boltzmann Selection
func boltzmannSelection(population []interface{}, fitnessValues []float64, temperature float64) interface{} {
	adjustedFitness := make([]float64, len(fitnessValues))
	for i, fitness := range fitnessValues {
		adjustedFitness[i] = math.Exp(fitness / temperature)
	}

	var totalFitness float64
	for _, fitness := range adjustedFitness {
		totalFitness += fitness
	}

	probabilities := make([]float64, len(adjustedFitness))
	for i, fitness := range adjustedFitness {
		probabilities[i] = fitness / totalFitness
	}

	cumulativeProbabilities := make([]float64, len(probabilities))
	cumulativeProbabilities[0] = probabilities[0]
	for i := 1; i < len(probabilities); i++ {
		cumulativeProbabilities[i] = cumulativeProbabilities[i-1] + probabilities[i]
	}

	rand.Seed(time.Now().UnixNano())
	randValue := rand.Float64()

	for i, cumulative := range cumulativeProbabilities {
		if randValue <= cumulative {
			return population[i]
		}
	}
	return nil
}

// Elitism Selection
func elitismSelection(population []interface{}, fitnessValues []float64, numElites int) []interface{} {
	eliteIndices := make([]int, numElites)
	for i := 0; i < numElites; i++ {
		maxFitness := -math.MaxFloat64
		maxIndex := -1
		for j, fitness := range fitnessValues {
			if fitness > maxFitness {
				maxFitness = fitness
				maxIndex = j
			}
		}
		eliteIndices[i] = maxIndex
		fitnessValues[maxIndex] = -math.MaxFloat64 // Mark this index as used
	}

	selected := make([]interface{}, numElites)
	for i, index := range eliteIndices {
		selected[i] = population[index]
	}
	return selected
}

// Random Selection
func randomSelection(population []interface{}) interface{} {
	rand.Seed(time.Now().UnixNano())
	return population[rand.Intn(len(population))]
}

// Fitness Sharing (for diversity)
func fitnessSharing(fitnessValues []float64, population []interface{}, sharingDistance float64) []float64 {
	sharedFitness := make([]float64, len(fitnessValues))
	for i, indiv := range population {
		sharingSum := 0.0
		for j, otherIndiv := range population {
			distance := math.Abs(float64(i - j)) // Assuming numerical representation
			if distance < sharingDistance {
				sharingSum += 1 - (distance / sharingDistance)
			}
		}
		sharedFitness[i] = fitnessValues[i] / sharingSum
	}
	return sharedFitness
}
