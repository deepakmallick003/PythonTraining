
# Find the vertex with minimum distance value, from the set of vertices not yet visited
def minDistance(dist, visited, V):
    min_val = float('infinity')
    min_index = -1
    for u in range(V):
        if dist[u] < min_val and not visited[u]:
            min_val = dist[u]
            min_index = u
    return min_index

# Dijkstra's algorithm to find the shortest path from a source vertex to all other vertices in a graph
def dijkstra(graph, src):
    V = len(graph)  # Number of vertices in the graph
    dist = [float('infinity')] * V  # Initialize distances with infinity
    dist[src] = 0  # Distance to source is 0
    visited = [False] * V  # Track visited vertices

    for _ in range(V):
        u = minDistance(dist, visited, V)  # Find the vertex with the minimum distance
        visited[u] = True  # Mark this vertex as visited
        for v in range(V):
            # Update distance if there's an edge and vertex v is not visited
            if graph[u][v] > 0 and not visited[v] and dist[v] > dist[u] + graph[u][v]:
                dist[v] = dist[u] + graph[u][v]  # Update distance

    print("Vertex \tDistance from Source")  # Print the results
    for i in range(V):
        print(f"{i} \t {dist[i]}")  # Print each vertex and its distance from source





import heapq

# Dijkstra's algorithm using a priority queue
def dijkstra(graph, src):
    V = len(graph)  # Number of vertices in the graph
    dist = [float('infinity')] * V  # Initialize distances with infinity
    dist[src] = 0  # Distance to source is 0
    pq = [(0, src)]  # Priority queue to hold vertices to be processed

    while pq:
        current_dist, u = heapq.heappop(pq)  # Get vertex with the smallest distance

        if current_dist > dist[u]:
            continue  # Skip if this distance is not the updated distance

        for v in range(V):
            if graph[u][v] > 0:  # If there is an edge from u to v
                distance = current_dist + graph[u][v]
                if distance < dist[v]:  # Update the distance if a shorter path is found
                    dist[v] = distance
                    heapq.heappush(pq, (distance, v))  # Push the vertex into the priority queue

    print("Vertex \tDistance from Source")  # Print the results
    for i in range(V):
        print(f"{i} \t {dist[i]}")  # Print each vertex and its distance from source

# Usage example
graph = [
    [0, 2, 6, 0, 0, 0, 0],  # Edges from node 0
    [2, 0, 0, 5, 0, 0, 0],  # Edges from node 1
    [6, 0, 0, 8, 0, 0, 0],  # Edges from node 2
    [0, 5, 8, 0, 10, 15, 0], # Edges from node 3
    [0, 0, 0, 10, 0, 0, 2], # Edges from node 4
    [0, 0, 0, 15, 0, 0, 6], # Edges from node 5
    [0, 0, 0, 0, 2, 6, 0]   # Edges from node 6
]

dijkstra(graph, 0)  # Execute Dijkstra's algorithm starting from vertex 0








# Usage example
graph = [
    [0, 2, 6, 0, 0, 0, 0],  # Edges from node 0
    [2, 0, 0, 5, 0, 0, 0],  # Edges from node 1
    [6, 0, 0, 8, 0, 0, 0],  # Edges from node 2
    [0, 5, 8, 0, 10, 15, 0], # Edges from node 3
    [0, 0, 0, 10, 0, 0, 2], # Edges from node 4
    [0, 0, 0, 15, 0, 0, 6], # Edges from node 5
    [0, 0, 0, 0, 2, 6, 0]   # Edges from node 6
]

dijkstra(graph, 0)  # Execute Dijkstra's algorithm starting from vertex 0
