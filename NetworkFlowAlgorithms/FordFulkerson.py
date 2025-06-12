from collections import deque

# Function to perform BFS to find an augmenting path
def bfs(capacity, source, sink, parent):
    visited = [False] * len(capacity)
    queue = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()
        
        for v in range(len(capacity)):
            if not visited[v] and capacity[u][v] > 0:  # If v is not visited and there's remaining capacity
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == sink:  # If we reach the sink, we have found an augmenting path
                    return True
    return False

# Ford-Fulkerson algorithm using BFS
def ford_fulkerson(capacity, source, sink):
    parent = [-1] * len(capacity)  # Stores the path from source to sink
    max_flow = 0
    
    # Augment the flow while there is a path from source to sink
    while bfs(capacity, source, sink, parent):
        path_flow = float('Inf')
        s = sink
        
        # Find the maximum flow through the path found by BFS
        while s != source:
            path_flow = min(path_flow, capacity[parent[s]][s])
            s = parent[s]
        
        # Update residual capacities of the edges and reverse edges along the path
        v = sink
        while v != source:
            u = parent[v]
            capacity[u][v] -= path_flow
            capacity[v][u] += path_flow
            v = parent[v]
        
        max_flow += path_flow  # Add path flow to overall flow
    
    return max_flow

# Example usage:
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

max_flow = ford_fulkerson(capacity_matrix, source, sink)
print(f"Max flow: {max_flow}")
