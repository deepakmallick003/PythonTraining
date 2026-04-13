def matrix_chain_order(dims):
    n = len(dims) - 1
    m = [[0] * n for _ in range(n)]
    
    for chain_len in range(2, n + 1):
        for i in range(n - chain_len + 1):
            j = i + chain_len - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if q < m[i][j]:
                    m[i][j] = q
    
    return m[0][n - 1]

# Example Usage
dims = [5, 4, 6, 2, 7]
print("Minimum number of multiplications:", matrix_chain_order(dims))
