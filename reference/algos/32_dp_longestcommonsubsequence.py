###############################

def lcs_recursive(X, Y, m, n):
    if m == 0 or n == 0:
        return 0
    elif X[m-1] == Y[n-1]:
        return 1 + lcs_recursive(X, Y, m-1, n-1)
    else:
        return max(lcs_recursive(X, Y, m-1, n), lcs_recursive(X, Y, m, n-1))

X = "ABCBDAB"
Y = "BDCAB"
print("Length of LCS is", lcs_recursive(X, Y, len(X), len(Y)))

###############################


def lcs_memoization(S1, S2, m, n, memo):
    if memo[m][n] != -1:
        return memo[m][n]
    if m == 0 or n == 0:
        memo[m][n] = 0
    elif S1[m-1] == S2[n-1]:
        memo[m][n] = 1 + lcs_memoization(S1, S2, m-1, n-1, memo)
    else:
        memo[m][n] = max(lcs_memoization(S1, S2, m-1, n, memo), lcs_memoization(S1, S2, m, n-1, memo))
    return memo[m][n]

# Example usage:
S1 = "AXYT"
S2 = "AYZX"
m = len(S1)
n = len(S2)
memo = [[-1] * (n + 1) for _ in range(m + 1)]
print("Length of LCS:", lcs_memoization(S1, S2, m, n, memo))


###############################

def lcs_tabulation(X, Y):
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i-1] == Y[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]

# Example usage:
X = "ABCBDAB"
Y = "BDCAB"
print("Length of LCS:", lcs_tabulation(X, Y))



###############################

def lcs_optimized(S1, S2):
    m, n = len(S1), len(S2)
    prev = [0] * (n + 1)
    
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if S1[i-1] == S2[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(prev[j], curr[j-1])
        prev = curr
    
    return prev[n]

# Example usage:
S1 = "AXYT"
S2 = "AYZX"
print("Length of LCS:", lcs_optimized(S1, S2))


###############################
