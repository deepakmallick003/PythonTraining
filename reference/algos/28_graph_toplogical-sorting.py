
#################Kahn's Algorith(BFS)######################

from collections import deque

def topological_sort_bfs_kahn(graph):
    V = len(graph)  # Number of vertices
    indegree = [0] * V  # Array to store the indegree of each vertex
    topo_order = []  # List to store the topological order

    # Calculate the indegree of each vertex
    for u in range(V):
        for v in graph[u]:
            indegree[v] += 1

    # Initialize the queue with all vertices with indegree 0
    queue = deque([i for i in range(V) if indegree[i] == 0])

    while queue:
        u = queue.popleft()
        topo_order.append(u)

        # Decrease the indegree of all adjacent vertices
        for v in graph[u]:
            indegree[v] -= 1
            # If indegree becomes 0, add to queue
            if indegree[v] == 0:
                queue.append(v)

    # Check if there was a cycle
    if len(topo_order) == V:
        return topo_order
    else:
        raise ValueError("Graph has at least one cycle")

# Example graph represented as an adjacency list
graph = [
    [1, 2],  # Vertex 0 points to vertices 1 and 2
    [3],     # Vertex 1 points to vertex 3
    [3],     # Vertex 2 points to vertex 3
    []       # Vertex 3 points to no other vertex
]

# Run topological sort
# print("Topological Sorting of the graph:", topological_sort_bfs_kahn(graph))





###################


############DFS based##############


def topological_sort_dfs(graph):
    def dfs(v):
        visited[v] = True
        for neighbor in graph[v]:
            if not visited[neighbor]:
                dfs(neighbor)
        stack.append(v)

    V = len(graph)
    visited = [False] * V
    stack = []

    for i in range(V):
        if not visited[i]:
            dfs(i)

    return stack[::-1]

# Example graph represented as an adjacency list
graph = [
    [],    # Vertex 0 points to no other vertex
    [],    # Vertex 1 points to no other vertex
    [3],   # Vertex 2 points to vertex 3
    [1],   # Vertex 3 points to vertex 1
    [0, 1],# Vertex 4 points to vertices 0 and 1
    [2, 0] # Vertex 5 points to vertices 2 and 0
]

# Run DFS-based topological sort
print("Topological Sorting of the graph:", topological_sort_dfs(graph))
