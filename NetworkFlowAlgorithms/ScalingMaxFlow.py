from collections import deque

# BFS to find the shortest augmenting path with capacity >= delta
def bfs(capacity, source, sink, parent, delta):
    visited = [False] * len(capacity)
    queue = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()
        
        for v in range(len(capacity)):
            # Only consider edges with capacity >= delta
            if not visited[v] and capacity[u][v] >= delta:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == sink:
                    return True
    
    return False

# Scaling Max-Flow algorithm
def scaling_max_flow(capacity, source, sink):
    max_flow = 0
    parent = [-1] * len(capacity)

    # Find the maximum capacity in the network to start scaling
    max_capacity = max(max(row) for row in capacity)

    # Start with the largest power of 2 <= max_capacity
    delta = 1
    while delta <= max_capacity:
        delta <<= 1
    delta >>= 1

    # While delta is >= 1, augment flow with paths of capacity >= delta
    while delta >= 1:
        while bfs(capacity, source, sink, parent, delta):
            # Find the bottleneck capacity in the augmenting path
            path_flow = float('Inf')
            v = sink
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, capacity[u][v])
                v = parent[v]

            # Augment flow along the path
            v = sink
            while v != source:
                u = parent[v]
                capacity[u][v] -= path_flow
                capacity[v][u] += path_flow
                v = parent[v]

            max_flow += path_flow
        
        # Reduce delta by half
        delta //= 2
    
    return max_flow

# Example usage
capacity_matrix = [
    [0, 16, 13, 0, 0, 0],
    [0, 0, 10, 12, 0, 0],
    [0, 4, 0, 0, 14, 0],
    [0, 0, 9, 0, 0, 20],
    [0, 0, 0, 7, 0, 4],
    [0, 0, 0, 0, 0, 0]
]

source = 0
sink = 5

max_flow = scaling_max_flow(capacity_matrix, source, sink)
print(f"Max flow: {max_flow}")
