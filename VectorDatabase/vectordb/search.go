package vectordb

import "sort"

// Distance holds a vector and its associated distance from the query vector.
type Distance[T Number] struct {
	Vector   Vector[T]
	Distance float64
}

// ByDistance implements sort.Interface for sorting distances.
type ByDistance[T Number] []Distance[T]

func (d ByDistance[T]) Len() int           { return len(d) }
func (d ByDistance[T]) Less(i, j int) bool { return d[i].Distance < d[j].Distance }
func (d ByDistance[T]) Swap(i, j int)      { d[i], d[j] = d[j], d[i] }

//Brute Force Search: This method involves computing the distance between the query vector and all vectors in the database, selecting the closest ones.
// BruteForceSearch finds the n nearest vectors to the query vector.
func BruteForceSearch[T Number](vectors []Vector[T], query Vector[T], n int) []Vector[T] {
	distances := make([]Distance[T], len(vectors))

	// Calculate the distance for each vector
	for i, vec := range vectors {
		dist := EuclideanDistance(vec, query)
		distances[i] = Distance[T]{Vector: vec, Distance: dist}
	}

	// Sort distances using the sort package
	sort.Sort(ByDistance[T](distances))

	// Return the n nearest vectors, ensuring not to exceed available distances
	if n > len(distances) {
		n = len(distances)
	}
	nearest := make([]Vector[T], n)
	for i := 0; i < n; i++ {
		nearest[i] = distances[i].Vector
	}
	return nearest
}

//KD-Trees: A space-partitioning data structure that organizes points in a k-dimensional space.

//Ball Trees: Similar to KD-Trees, Ball Trees partition data points into hyperspheres (balls),

//Hierarchical Navigable Small World (HNSW): A graph-based approach that constructs a small world graph for efficient searching.

//Product Quantization: This method reduces the dimensionality of vectors and quantizes them

//IVF (Inverted File) Indexing: This method divides the dataset into clusters and performs searches within each cluster to reduce the search space.
