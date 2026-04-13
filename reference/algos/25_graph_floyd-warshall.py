# Number of vertices in the graph
V = 4

# Define infinity as a large enough value. This will be used for vertices not connected by an edge.
INF = float('inf')

# A utility function to print the solution
def print_solution(dist):
    print("Shortest distances between every pair of vertices:")
    for i in range(V):
        for j in range(V):
            if dist[i][j] == INF:
                print("INF", end=" ")
            else:
                print(dist[i][j], end="  ")
        print(" ")

# Solves the all-pairs shortest path problem using Floyd-Warshall algorithm
def floyd_warshall(graph):
    # dist[][] will be the output matrix that will eventually have the shortest distances between every pair of vertices
    dist = [[INF] * V for _ in range(V)]

    # Initialize the solution matrix same as input graph matrix.
    for i in range(V):
        for j in range(V):
            dist[i][j] = graph[i][j]

    # Step 2: Add all vertices one by one to the set of intermediate vertices.
    for k in range(V):
        # Treating k as an intermediate vertex
        for i in range(V):
            for j in range(V):
                # Update dist[i][j] if a shorter path is found through vertex k
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    print_solution(dist)

# Example graph represented as an adjacency matrix
graph = [
    [0, 3, INF, 7],
    [8, 0, 2, INF],
    [5, INF, 0, 1],
    [2, INF, INF, 0]
]

# Run Floyd-Warshall algorithm
floyd_warshall(graph)
