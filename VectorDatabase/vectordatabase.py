import numpy as np
from scipy.spatial import distance

class VectorDatabase:
    def __init__(self):
        self.vectors = []
        self.metadata = []  # Optional: to store additional data related to vectors

    def add_vector(self, vector, meta=None):
        """Add a new vector to the database."""
        if not isinstance(vector, np.ndarray):
            vector = np.array(vector)
        self.vectors.append(vector)
        self.metadata.append(meta)

    def query(self, vector, k=1):
        """Query the database for the k nearest neighbors to the input vector."""
        if not isinstance(vector, np.ndarray):
            vector = np.array(vector)

        # Calculate distances from the query vector to all vectors in the database
        distances = distance.cdist([vector], self.vectors, 'euclidean')[0]
        
        # Get the indices of the k nearest neighbors
        nearest_indices = np.argsort(distances)[:k]
        nearest_vectors = [self.vectors[i] for i in nearest_indices]
        nearest_metadata = [self.metadata[i] for i in nearest_indices]

        return nearest_vectors, nearest_metadata, distances[nearest_indices]

    def remove_vector(self, index):
        """Remove a vector from the database by index."""
        if 0 <= index < len(self.vectors):
            del self.vectors[index]
            del self.metadata[index]
        else:
            raise IndexError("Index out of range.")

    def __len__(self):
        """Return the number of vectors in the database."""
        return len(self.vectors)

# Example usage
if __name__ == "__main__":
    db = VectorDatabase()

    # Adding some vectors
    db.add_vector([1.0, 2.0, 3.0], meta="Vector 1")
    db.add_vector([4.0, 5.0, 6.0], meta="Vector 2")
    db.add_vector([7.0, 8.0, 9.0], meta="Vector 3")

    # Querying for the nearest vector
    query_vector = [5.0, 5.0, 5.0]
    nearest_vectors, metadata, distances = db.query(query_vector, k=2)

    print("Nearest Vectors:", nearest_vectors)
    print("Metadata:", metadata)
    print("Distances:", distances)
