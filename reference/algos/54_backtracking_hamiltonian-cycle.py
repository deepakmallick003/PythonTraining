def is_safe(v, graph, path, pos):
    # Check if this vertex is an adjacent vertex of the previously added vertex.
    if graph[path[pos - 1]][v] == 0:
        return False
    
    # Check if the vertex has already been included in the path.
    if v in path:
        return False
    
    return True

def hamiltonian_cycle_util(graph, path, pos):
    # Base case: If all vertices are included in the cycle
    if pos == len(graph):
        # Check if the last vertex is adjacent to the first vertex
        if graph[path[pos - 1]][path[0]] == 1:
            return True
        else:
            return False

    # Try different vertices as the next candidate
    for v in range(1, len(graph)):
        if is_safe(v, graph, path, pos):
            path[pos] = v

            if hamiltonian_cycle_util(graph, path, pos + 1):
                return True

            # Backtrack
            path[pos] = -1
    
    return False

def hamiltonian_cycle(graph):
    n = len(graph)
    path = [-1] * n

    # Start from the first vertex
    path[0] = 0

    if not hamiltonian_cycle_util(graph, path, 1):
        print("No Hamiltonian Cycle found")
        return False

    print("Hamiltonian Cycle found:", path + [path[0]])
    return True

# Example graph represented as an adjacency matrix
graph = [
    [0, 1, 0, 1, 1],
    [1, 0, 1, 1, 0],
    [0, 1, 0, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 1, 1, 0]
]

hamiltonian_cycle(graph)
