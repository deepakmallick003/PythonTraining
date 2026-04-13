def dfs_iterative(graph, start):
    visited = set()
    stack = [start]

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            print(vertex, end=' ')
            visited.add(vertex)
            stack.extend(neighbor for neighbor in graph[vertex] if neighbor not in visited)


def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = set()

    # Mark the current node as visited
    visited.add(node)
    print(node, end=' ')

    # Recur for all the vertices adjacent to this vertex
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

# Example usage
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print("\nDFS iterative traversal starting from node A:")
dfs_iterative(graph, 'A')

print("\nDFS recursive traversal starting from node A:")
dfs_recursive(graph, 'A')

