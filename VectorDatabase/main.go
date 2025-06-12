package main

import (
	"fmt"
	vectordb "vectordatabase/vectordb"
)

func main() {
	// Create a new instance of DatabaseDenseVector
	db := &vectordb.DatabaseDenseVector[float64]{Vectors: make([]vectordb.DenseVector[float64], 0)}

	// Add vectors to the database
	db.AddVector("vec1", []float64{1.0, 2.0, 3.0})
	db.AddVector("vec2", []float64{4.0, 5.0, 6.0})
	db.AddVector("vec3", []float64{7.0, 8.0, 9.0})
	db.AddVector("vec3", []float64{2.0, 1.0, 1.0})
	db.AddVector("vec3", []float64{10.0, 9.0, 7.0})

	// Create a query vector
	query := vectordb.DenseVector[float64]{ID: "queryVec", Values: []float64{10.0, 3.0, 10.0}}

	// Convert the map to a slice of vectors for the search
	vectors := make([]vectordb.Vector[float64], 0, len(db.Vectors))
	for _, vec := range db.Vectors {
		vectors = append(vectors, vec)
	}

	// Perform the brute force search
	nearestVectors := vectordb.BruteForceSearch(vectors, query, 2)

	// Output the nearest vectors
	for _, vec := range nearestVectors {
		fmt.Printf("Nearest Vector ID: %s, Values: %v\n", vec.GetID(), vec.GetDenseValues())
	}
}
