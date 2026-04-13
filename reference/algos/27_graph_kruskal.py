class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1


def kruskal_algorithm(graph):
    V = len(graph)
    edges = []

    # Convert the adjacency matrix to a list of edges
    for u in range(V):
        for v in range(u, V):
            if graph[u][v] != 0:
                edges.append((graph[u][v], u, v))

    # Sort the edges by their weight
    edges.sort()

    uf = UnionFind(V)
    mst = []

    for weight, u, v in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst.append((u, v, weight))
            if len(mst) == V - 1:
                break

    # Print the edges in the MST
    print("Edge \tWeight")
    for u, v, weight in mst:
        print(f"{u} - {v} \t {weight}")

# Example graph represented as an adjacency matrix
graph = [
    [0, 2, 0, 6, 0],
    [2, 0, 3, 8, 5],
    [0, 3, 0, 0, 7],
    [6, 8, 0, 0, 9],
    [0, 5, 7, 9, 0]
]

# Run Kruskal's algorithm
kruskal_algorithm(graph)
