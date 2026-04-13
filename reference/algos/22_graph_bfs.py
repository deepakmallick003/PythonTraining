def bfs_iterative(graph, start):
    visited = set()
    queue = [start]
    visited.add(start)
    print(start, end=' ')

    while queue:
        vertex = queue.pop(0)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                print(neighbor, end=' ')
                visited.add(neighbor)
                queue.append(neighbor)




# Example usage
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print("\BFS iterative traversal starting from node A:")
bfs_iterative(graph, 'A')


