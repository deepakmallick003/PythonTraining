def nearest_neighbor_tsp(graph, start):
    n = len(graph)
    visited = [False] * n
    visited[start] = True
    route = [start]
    total_distance = 0
    current_city = start
    
    while len(route) < n:
        nearest_city = None
        shortest_distance = float('inf')
        
        for next_city in range(n):
            if not visited[next_city] and graph[current_city][next_city] < shortest_distance:
                shortest_distance = graph[current_city][next_city]
                nearest_city = next_city
        
        route.append(nearest_city)
        visited[nearest_city] = True
        total_distance += shortest_distance
        current_city = nearest_city
    
    total_distance += graph[current_city][start]  # return to starting city
    route.append(start)
    
    return route, total_distance


# Example usage:
graph = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]
print(nearest_neighbor_tsp(graph))




def tsp_held_karp(graph):
    n = len(graph)
    dp = {}

    def visit(mask, pos):
        if (mask, pos) in dp:
            return dp[(mask, pos)]
        if mask == (1 << n) - 1:  # all cities visited
            return graph[pos][0]
        ans = float('inf')
        for city in range(n):
            if mask & (1 << city) == 0:  # if city is unvisited
                ans = min(ans, graph[pos][city] + visit(mask | (1 << city), city))
        dp[(mask, pos)] = ans
        return ans

    return visit(1, 0)

# Example usage:
graph = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]
print(tsp_held_karp(graph))
