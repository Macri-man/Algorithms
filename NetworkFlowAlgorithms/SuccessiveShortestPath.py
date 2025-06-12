import heapq

# Find the shortest path using Dijkstra's algorithm with reduced costs
def dijkstra(capacity, cost, source, potential):
    n = len(capacity)
    dist = [float('inf')] * n
    parent = [-1] * n
    dist[source] = 0

    # Priority queue to store (distance, vertex)
    pq = [(0, source)]

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist[u]:
            continue

        # Explore the neighbors
        for v in range(n):
            if capacity[u][v] > 0:
                # Reduced cost = original cost + potential difference
                reduced_cost = cost[u][v] + potential[u] - potential[v]
                if dist[v] > dist[u] + reduced_cost:
                    dist[v] = dist[u] + reduced_cost
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))

    return dist, parent

# Successive Shortest Path algorithm for min-cost flow
def successive_shortest_path(capacity, cost, source, sink, demand):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    potential = [0] * n
    total_cost = 0

    while demand > 0:
        # Find shortest augmenting path with reduced costs
        dist, parent = dijkstra(capacity, cost, source, potential)

        # No more augmenting paths, terminate
        if dist[sink] == float('inf'):
            break

        # Calculate the bottleneck capacity (smallest residual capacity)
        bottleneck = demand
        v = sink
        while v != source:
            u = parent[v]
            bottleneck = min(bottleneck, capacity[u][v])
            v = parent[v]

        # Send the flow along the augmenting path
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += bottleneck
            capacity[u][v] -= bottleneck
            capacity[v][u] += bottleneck  # reverse edge in residual graph
            total_cost += bottleneck * cost[u][v]
            v = parent[v]

        # Update the remaining demand
        demand -= bottleneck

        # Update potentials
        for i in range(n):
            if dist[i] < float('inf'):
                potential[i] += dist[i]

    return flow, total_cost

# Example usage
capacity_matrix = [
    [0, 5, 3, 0, 0, 0],
    [0, 0, 0, 7, 4, 0],
    [0, 3, 0, 3, 0, 2],
    [0, 0, 0, 0, 0, 5],
    [0, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 0, 0]
]

cost_matrix = [
    [0, 2, 4, 0, 0, 0],
    [0, 0, 0, 3, 2, 0],
    [0, 1, 0, 2, 0, 3],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 0]
]

source = 0
sink = 5
demand = 5

flow, total_cost = successive_shortest_path(capacity_matrix, cost_matrix, source, sink, demand)
print(f"Flow: {flow}")
print(f"Total cost: {total_cost}")
