from collections import defaultdict

def kosaraju_scc(graph):
    def dfs(v, visited, stack):
        visited[v] = True
        for neighbor in graph[v]:
            if not visited[neighbor]:
                dfs(neighbor, visited, stack)
        stack.append(v)

    def reverse_graph(graph):
        reversed_graph = defaultdict(list)
        for src in graph:
            for dest in graph[src]:
                reversed_graph[dest].append(src)
        return reversed_graph

    def dfs_collect(v, visited, component, graph):
        visited[v] = True
        component.append(v)
        for neighbor in graph[v]:
            if not visited[neighbor]:
                dfs_collect(neighbor, visited, component, graph)

    stack = []
    visited = [False] * len(graph)

    # Step 2: DFS on the original graph to compute finishing times
    for v in range(len(graph)):
        if not visited[v]:
            dfs(v, visited, stack)

    # Step 1: Reverse the graph
    reversed_graph = reverse_graph(graph)
    visited = [False] * len(graph)
    scc = []

    # Step 3: DFS on the reversed graph to find SCCs
    while stack:
        v = stack.pop()
        if not visited[v]:
            component = []
            dfs_collect(v, visited, component, reversed_graph)
            scc.append(component)

    return scc

# Example graph represented as an adjacency list
graph = {
    0: [1],
    1: [2],
    2: [0, 3],
    3: [4],
    4: [5, 7],
    5: [6],
    6: [4],
    7: []
}

print("Strongly Connected Components:", kosaraju_scc(graph))
