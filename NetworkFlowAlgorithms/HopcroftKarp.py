from collections import deque

# Hopcroft-Karp Algorithm for Maximum Bipartite Matching
class HopcroftKarp:
    def __init__(self, U, V, edges):
        self.U = U  # Left set of vertices
        self.V = V  # Right set of vertices
        self.edges = edges  # Adjacency list for the bipartite graph

        self.pair_U = [-1] * U  # Pairing for U vertices
        self.pair_V = [-1] * V  # Pairing for V vertices
        self.dist = [-1] * U    # Distance for BFS

    # Perform BFS to find the shortest augmenting path
    def bfs(self):
        queue = deque()
        for u in range(self.U):
            if self.pair_U[u] == -1:  # Unmatched vertex in U
                self.dist[u] = 0
                queue.append(u)
            else:
                self.dist[u] = float('inf')

        found_augmenting_path = False

        while queue:
            u = queue.popleft()

            if self.dist[u] >= float('inf'):
                continue

            # Explore neighbors of u
            for v in self.edges[u]:
                if self.pair_V[v] == -1:
                    found_augmenting_path = True  # Found an augmenting path
                else:
                    next_u = self.pair_V[v]
                    if self.dist[next_u] == float('inf'):
                        self.dist[next_u] = self.dist[u] + 1
                        queue.append(next_u)

        return found_augmenting_path

    # Perform DFS to find and augment the path
    def dfs(self, u):
        if u == -1:
            return True

        for v in self.edges[u]:
            next_u = self.pair_V[v]
            if self.dist[next_u] == self.dist[u] + 1 and self.dfs(next_u):
                self.pair_U[u] = v
                self.pair_V[v] = u
                return True

        self.dist[u] = float('inf')
        return False

    # Main function to find the maximum matching
    def maximum_matching(self):
        matching_size = 0

        # Repeat until no more augmenting paths are found
        while self.bfs():
            for u in range(self.U):
                if self.pair_U[u] == -1 and self.dfs(u):
                    matching_size += 1

        return matching_size


# Example usage
U = 4  # Number of vertices in set U
V = 4  # Number of vertices in set V
edges = {
    0: [0, 1],
    1: [1, 2],
    2: [2],
    3: [0, 3]
}

hk = HopcroftKarp(U, V, edges)
max_matching = hk.maximum_matching()
print(f"Maximum Matching Size: {max_matching}")
