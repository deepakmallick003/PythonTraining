####Using Arrays###

def prims_algorithm(graph):
    V = len(graph)  # Number of vertices in the graph

    # Initialize all keys as INFINITE and MST set as False
    key = [float('inf')] * V
    parent = [-1] * V  # Array to store the constructed MST
    key[0] = 0  # Make key 0 so that this vertex is picked as the first vertex
    mstSet = [False] * V

    for _ in range(V):
        # Pick the minimum key vertex from the set of vertices not yet included in MST
        u = min_key(key, mstSet)

        # Add the picked vertex to the MST set
        mstSet[u] = True

        # Update key and parent index of the adjacent vertices of the picked vertex
        for v in range(V):
            if graph[u][v] > 0 and not mstSet[v] and key[v] > graph[u][v]:
                key[v] = graph[u][v]
                parent[v] = u

    # Print function to display the constructed MST
    print("Edge \tWeight")
    for i in range(1, V):
        print(parent[i], "-", i, "\t", graph[i][parent[i]])

def min_key(key, mstSet):
    min_val = float('inf')
    min_index = -1

    for v in range(len(key)):
        if key[v] < min_val and not mstSet[v]:
            min_val = key[v]
            min_index = v

    return min_index

# Example graph represented as an adjacency matrix
graph = [
    [0, 2, 0, 6, 0],
    [2, 0, 3, 8, 5],
    [0, 3, 0, 0, 7],
    [6, 8, 0, 0, 9],
    [0, 5, 7, 9, 0]
]

# Run Prim's algorithm
prims_algorithm(graph)



#####################


#####using HeapQ#####

import heapq

def prims_algorithm_with_pq(graph):
    V = len(graph)
    mstSet = [False] * V
    edge_count = 0
    min_heap = [(0, 0)]  # (weight, vertex)
    parent = [-1] * V
    key = [float('inf')] * V
    key[0] = 0

    while edge_count < V - 1:
        weight, u = heapq.heappop(min_heap)
        if mstSet[u]:
            continue
        mstSet[u] = True
        edge_count += 1

        for v in range(V):
            if graph[u][v] and not mstSet[v] and graph[u][v] < key[v]:
                key[v] = graph[u][v]
                parent[v] = u
                heapq.heappush(min_heap, (graph[u][v], v))

    print("Edge \tWeight")
    for i in range(1, V):
        print(parent[i], "-", i, "\t", graph[i][parent[i]])

# Example graph represented as an adjacency matrix
graph = [
    [0, 2, 0, 6, 0],
    [2, 0, 3, 8, 5],
    [0, 3, 0, 0, 7],
    [6, 8, 0, 0, 9],
    [0, 5, 7, 9, 0]
]

# Run Prim's algorithm with priority queue
prims_algorithm_with_pq(graph)

#####################

