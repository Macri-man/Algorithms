package main

import (
	"math/rand"
)

// Binary Chromosomes
func createBinaryChromosome(length int) []int {
	chromosome := make([]int, length)
	for i := 0; i < length; i++ {
		chromosome[i] = rand.Intn(2) // 0 or 1
	}
	return chromosome
}

// Integer Chromosomes
func createIntegerChromosome(length, minVal, maxVal int) []int {
	chromosome := make([]int, length)
	for i := 0; i < length; i++ {
		chromosome[i] = rand.Intn(maxVal-minVal+1) + minVal
	}
	return chromosome
}

// Floating-Point Chromosomes
func createFloatChromosome(length int, minVal, maxVal float64) []float64 {
	chromosome := make([]float64, length)
	for i := 0; i < length; i++ {
		chromosome[i] = rand.Float64()*(maxVal-minVal) + minVal
	}
	return chromosome
}

// Permutation Chromosomes
func createPermutationChromosome(elements []int) []int {
	chromosome := make([]int, len(elements))
	copy(chromosome, elements)

	// Shuffle the chromosome
	for i := range chromosome {
		j := rand.Intn(i + 1)
		chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
	}
	return chromosome
}

// Tree Chromosomes
type TreeNode struct {
	Value       interface{}
	Left, Right *TreeNode
}

func createTreeChromosome(depth int, operators, operands []interface{}) *TreeNode {
	if depth == 0 {
		return &TreeNode{Value: operands[rand.Intn(len(operands))]}
	}
	operator := operators[rand.Intn(len(operators))]
	left := createTreeChromosome(depth-1, operators, operands)
	right := createTreeChromosome(depth-1, operators, operands)
	return &TreeNode{Value: operator, Left: left, Right: right}
}

// Vector Chromosomes
func createVectorChromosome(length int) []float64 {
	chromosome := make([]float64, length)
	for i := 0; i < length; i++ {
		chromosome[i] = rand.Float64()
	}
	return chromosome
}

// Graph-Based Chromosomes
func createGraphChromosome(numNodes, numEdges int) map[int][]int {
	graph := make(map[int][]int)
	edges := make(map[[2]int]struct{})

	for len(edges) < numEdges {
		u, v := rand.Intn(numNodes), rand.Intn(numNodes)
		if u != v && !edgeExists(u, v, edges) {
			edges[[2]int{u, v}] = struct{}{}
			graph[u] = append(graph[u], v)
			graph[v] = append(graph[v], u)
		}
	}

	return graph
}

// Helper function to check if an edge exists in the graph
func edgeExists(u, v int, edges map[[2]int]struct{}) bool {
	_, exists := edges[[2]int{u, v}]
	_, reverseExists := edges[[2]int{v, u}]
	return exists || reverseExists
}
