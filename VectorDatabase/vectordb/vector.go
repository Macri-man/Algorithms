package vectordb

import "fmt"

// Vector is an interface that represents a generic vector.
type Vector[T Number] interface {
	GetID() string        // Retrieve the ID of the vector
	GetValues() map[int]T // Retrieve the values of the vector (sparse representation)
	GetDenseValues() []T  // Retrieve the values of the vector (dense representation)
	Dimensions() int      // Get the number of dimensions of the vector
}

// Number is a type constraint that allows int, float32, and float64
type Number interface {
	int | int64 | float32 | float64
}

// Vector represents a high-dimensional vector with generic number type
type DenseVector[T Number] struct {
	ID     string
	Values []T
}

// GetID returns the ID of the DenseVector.
func (v DenseVector[T]) GetID() string {
	return v.ID
}

// GetValues returns the dense representation as a map (can return nil if not applicable).
func (v DenseVector[T]) GetValues() map[int]T {
	return nil // Dense vectors do not have a sparse representation
}

// GetDenseValues returns the values of the DenseVector.
func (v DenseVector[T]) GetDenseValues() []T {
	return v.Values
}

// Dimensions returns the number of dimensions of the DenseVector.
func (v DenseVector[T]) Dimensions() int {
	return len(v.Values)
}

// VectorDatabase is an interface that defines methods for interacting with a vector database.
type VectorDatabase[T Number] interface {
	AddVector(id string, values []T) error
	RemoveVector(id string) (bool, error)
	GetDimensions() (int, error)
	GetVector(id string) (Vector[T], error)
}

// Database represents a simple in-memory vector database with generic number type
type DatabaseDenseVector[T Number] struct {
	Vectors []DenseVector[T]
}

// AddVector adds a new dense vector (with slice values) to the database
func (db *DatabaseDenseVector[T]) AddVector(id string, values []T) {
	vector := DenseVector[T]{
		ID:     id,
		Values: values,
	}
	db.Vectors = append(db.Vectors, vector) // Append to Vectors slice
}

// RemoveVector removes a vector from the database by its ID
func (db *DatabaseDenseVector[T]) RemoveVector(id string) bool {
	for i, v := range db.Vectors {
		if v.ID == id {
			// Remove vector by slicing the slice
			db.Vectors = append(db.Vectors[:i], db.Vectors[i+1:]...)
			return true // Return true if the vector was found and removed
		}
	}
	return false // Return false if the vector was not found
}

// GetDimensions retrieves the current dimensions of the vectors.
func (db *DatabaseDenseVector[T]) GetDimensions() (int, error) {
	if len(db.Vectors) == 0 {
		return 0, fmt.Errorf("no vectors in the database")
	}
	return len(db.Vectors[0].Values), nil
}

// GetVector retrieves a dense vector by its ID.
func (db *DatabaseDenseVector[T]) GetVector(id string) (DenseVector[T], error) {
	for _, v := range db.Vectors {
		if v.ID == id {
			return v, nil // Return the found vector
		}
	}
	return DenseVector[T]{}, fmt.Errorf("vector with ID %s not found", id) // Return an error if not found
}

// Vector represents a sparse high-dimensional vector using a map
type SparseVector[T Number] struct {
	ID     string
	Values map[int]T // key: dimension index, value: the value at that dimension
}

// GetID returns the ID of the SparseVector.
func (v SparseVector[T]) GetID() string {
	return v.ID
}

// GetValues returns the values of the SparseVector as a map.
func (v SparseVector[T]) GetValues() map[int]T {
	return v.Values
}

// GetDenseValues returns the values of the SparseVector as a dense representation.
func (v SparseVector[T]) GetDenseValues() []T {
	// Create a dense representation of the sparse vector
	maxIndex := -1
	for index := range v.Values {
		if index > maxIndex {
			maxIndex = index
		}
	}

	dense := make([]T, maxIndex+1) // Create a dense slice
	for index, value := range v.Values {
		dense[index] = value
	}
	return dense
}

// Dimensions returns the number of dimensions of the SparseVector.
func (v SparseVector[T]) Dimensions() int {
	maxIndex := -1
	for index := range v.Values {
		if index > maxIndex {
			maxIndex = index
		}
	}
	return maxIndex + 1 // Dimensions are 0-indexed
}

// Database represents a simple in-memory vector database with generic number type
type DatabaseSparseVector[T Number] struct {
	Vectors []SparseVector[T]
}

// AddVector adds a new sparse vector (with map values) to the database
func (db *DatabaseSparseVector[T]) AddVector(id string, values map[int]T) {
	vector := SparseVector[T]{
		ID:     id,     // Ensure ID is assigned here
		Values: values, // Expecting a map here
	}
	db.Vectors = append(db.Vectors, vector) // Append to Vectors slice
}

// RemoveVector removes a vector from the database by its ID
func (db *DatabaseSparseVector[T]) RemoveVector(id string) bool {
	for i, v := range db.Vectors {
		if v.ID == id {
			// Remove vector by slicing the slice
			db.Vectors = append(db.Vectors[:i], db.Vectors[i+1:]...)
			return true // Return true if the vector was found and removed
		}
	}
	return false // Return false if the vector was not found
}

// GetDimensions retrieves the current dimensions of the sparse vectors in the database.
func (db *DatabaseSparseVector[T]) GetDimensions() (int, error) {
	if len(db.Vectors) == 0 {
		return 0, fmt.Errorf("no vectors in the database")
	}

	// Calculate dimensions based on the largest index in the Values map
	maxIndex := -1
	for _, v := range db.Vectors {
		for index := range v.Values {
			if index > maxIndex {
				maxIndex = index
			}
		}
	}
	return maxIndex + 1, nil // Dimensions are 0-indexed, so add 1 for the total count
}

// GetVector retrieves a sparse vector by its ID.
func (db *DatabaseSparseVector[T]) GetVector(id string) (SparseVector[T], error) {
	for _, v := range db.Vectors {
		if v.ID == id {
			return v, nil // Return the found vector
		}
	}
	return SparseVector[T]{}, fmt.Errorf("vector with ID %s not found", id) // Return an error if not found
}
