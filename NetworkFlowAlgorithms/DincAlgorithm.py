from collections import deque

# BFS to build level graph
def bfs(capacity, source, sink, level):
    queue = deque([source])
    level[source] = 0

    while queue:
        u = queue.popleft()
        for v in range(len(capacity)):
            if level[v] < 0 and capacity[u][v] > 0:  # If v is unvisited and there is residual capacity
                level[v] = level[u] + 1
                queue.append(v)
    
    return level[sink] >= 0  # Return True if sink is reachable

# DFS to send flow through level graph
def dfs(capacity, u, sink, flow, level, start):
    if u == sink:
        return flow  # If we reach the sink, return the flow

    while start[u] < len(capacity):
        v = start[u]
        if level[v] == level[u] + 1 and capacity[u][v] > 0:  # Valid path in the level graph
            curr_flow = min(flow, capacity[u][v])
            temp_flow = dfs(capacity, v, sink, curr_flow, level, start)
            
            if temp_flow > 0:  # If we were able to push flow
                capacity[u][v] -= temp_flow  # Update forward capacity
                capacity[v][u] += temp_flow  # Update reverse capacity
                return temp_flow
        
        start[u] += 1  # Move to next vertex

    return 0  # If no flow could be sent

# Dinic's Algorithm
def dinic(capacity, source, sink):
    max_flow = 0
    level = [-1] * len(capacity)  # Level graph
    
    while bfs(capacity, source, sink, level):  # Build the level graph using BFS
        start = [0] * len(capacity)  # Track the starting point for each node in DFS
        while True:
            flow = dfs(capacity, source, sink, float('Inf'), level, start)  # Send flow using DFS
            if flow == 0:
                break  # No more augmenting paths, move to next BFS level graph
            max_flow += flow
        
        level = [-1] * len(capacity)  # Reset level after each blocking flow
    
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

max_flow = dinic(capacity_matrix, source, sink)
print(f"Max flow: {max_flow}")
