package vectordb

import (
	"fmt"
	"math"
)

// DotProduct calculates the dot product of two vectors.
func DotProduct[T Number](a, b Vector[T]) (float64, error) {
	if a.Dimensions() != b.Dimensions() {
		return 0, fmt.Errorf("vectors must be of the same length")
	}

	dotProduct := 0.0
	for i := 0; i < a.Dimensions(); i++ {
		dotProduct += float64(a.GetDenseValues()[i]) * float64(b.GetDenseValues()[i])
	}

	return dotProduct, nil
}

// CosineSimilarity measures the cosine of the angle between two vectors.
func CosineSimilarity[T Number](a, b Vector[T]) (float64, error) {
	if a.Dimensions() != b.Dimensions() {
		return 0.0, fmt.Errorf("vectors must be of the same length")
	}

	dotProduct, err := DotProduct(a, b)
	if err != nil {
		return 0.0, err
	}

	magnitudeA := 0.0
	magnitudeB := 0.0

	for i := 0; i < a.Dimensions(); i++ {
		magnitudeA += float64(a.GetDenseValues()[i]) * float64(a.GetDenseValues()[i])
		magnitudeB += float64(b.GetDenseValues()[i]) * float64(b.GetDenseValues()[i])
	}

	if magnitudeA == 0 || magnitudeB == 0 {
		return 0.0, fmt.Errorf("magnitude of vector cannot be zero")
	}

	return dotProduct / (math.Sqrt(magnitudeA) * math.Sqrt(magnitudeB)), nil
}

// EuclideanDistance calculates the Euclidean distance between two vectors.
func EuclideanDistance[T Number](a, b Vector[T]) float64 {
	if a.Dimensions() != b.Dimensions() {
		// Return a large distance if dimensions don't match
		return math.MaxFloat64
	}

	sum := 0.0
	for i := 0; i < a.Dimensions(); i++ {
		diff := float64(a.GetDenseValues()[i]) - float64(b.GetDenseValues()[i])
		sum += diff * diff
	}
	return math.Sqrt(sum)
}

//Manhattan Distance (L1 Norm)  it measures the distance by summing the absolute differences of vector components.

//Jaccard Similarity  Compares the intersection over the union of two sets or binary vectors. It is especially used for sparse binary vectors.

//Hamming Distance Measures the number of positions where two vectors differ. It's used primarily for binary vectors or strings of equal length.

//Minkowski Distance A generalization of both Euclidean and Manhattan distances.

//Chebyshev Distance Measures the maximum absolute difference between vector coordinates. It is useful for determining bounds in grids.

//Mahalanobis Distance Accounts for correlations between features. It is especially useful when the data is not isotropic or has varying variances along different dimensions.
