###############################

def edit_distance_recursive(str1, str2, m, n):
    if m == 0:
        return n
    if n == 0:
        return m
    
    if str1[m-1] == str2[n-1]:
        return edit_distance_recursive(str1, str2, m-1, n-1)
    
    return 1 + min(edit_distance_recursive(str1, str2, m, n-1),    # Insert
                   edit_distance_recursive(str1, str2, m-1, n),    # Delete
                   edit_distance_recursive(str1, str2, m-1, n-1))  # Replace

# Example usage:
str1 = "kitten"
str2 = "sitting"
print("Edit Distance:", edit_distance_recursive(str1, str2, len(str1), len(str2)))

###############################

def edit_distance_memoization(str1, str2, m, n, memo):
    if memo[m][n] != -1:
        return memo[m][n]
    
    if m == 0:
        memo[m][n] = n
    elif n == 0:
        memo[m][n] = m
    elif str1[m-1] == str2[n-1]:
        memo[m][n] = edit_distance_memoization(str1, str2, m-1, n-1, memo)
    else:
        memo[m][n] = 1 + min(edit_distance_memoization(str1, str2, m, n-1, memo),    # Insert
                             edit_distance_memoization(str1, str2, m-1, n, memo),    # Delete
                             edit_distance_memoization(str1, str2, m-1, n-1, memo))  # Replace
    
    return memo[m][n]

# Example usage:
str1 = "kitten"
str2 = "sitting"
m = len(str1)
n = len(str2)
memo = [[-1] * (n + 1) for _ in range(m + 1)]
print("Edit Distance:", edit_distance_memoization(str1, str2, m, n, memo))


###############################

def edit_distance_tabulation(str1, str2):
    m = len(str1)
    n = len(str2)
    
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1],    # Insert
                                   dp[i-1][j],    # Delete
                                   dp[i-1][j-1])  # Replace
    
    return dp[m][n]

# Example usage:
str1 = "kitten"
str2 = "sitting"
print("Edit Distance:", edit_distance_tabulation(str1, str2))


###############################

