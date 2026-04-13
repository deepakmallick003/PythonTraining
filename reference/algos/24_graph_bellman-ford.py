def bellman_ford(graph, V, E, src):
    # Step 1: Initialize distances from src to all other vertices as INFINITE
    dist = [float('infinity')] * V
    dist[src] = 0

    # Step 2: Relax all edges |V| - 1 times.
    for _ in range(V - 1):
        for u, v, w in graph:
            if dist[u] != float('infinity') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Step 3: Check for negative-weight cycles.
    for u, v, w in graph:
        if dist[u] != float('infinity') and dist[u] + w < dist[v]:
            print("Graph contains negative weight cycle")
            return

    print("Vertex Distance from Source")
    for i in range(V):
        print(f"{i}\t\t{dist[i]}")

# Example graph as a list of edges
graph = [
    (0, 1, -1),
    (0, 2, 4),
    (1, 2, 3),
    (1, 3, 2),
    (1, 4, 2),
    (3, 2, 5),
    (3, 1, 1),
    (4, 3, -3)
]

V = 5  # Number of vertices in graph
E = len(graph)  # Number of edges in graph

bellman_ford(graph, V, E, 0)
