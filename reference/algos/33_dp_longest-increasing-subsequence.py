###############################

def lis_end_at_i(arr, i):
    # Base case
    if i == 0:
        return 1

    mx = 1
    for prev in range(i):
        if arr[prev] < arr[i]:
            mx = max(mx, lis_end_at_i(arr, prev) + 1)
    return mx

def lis_recursive(arr):
    n = len(arr)
    res = 1
    for i in range(1, n):
        res = max(res, lis_end_at_i(arr, i))
    return res

# Example usage:
arr = [10, 22, 9, 33, 21, 50, 41, 60, 80]
print("Length of LIS:", lis_recursive(arr))

###############################

def lis_memoization(arr):
    n = len(arr)
    memo = [-1] * n
    
    def lis_ending_at(i):
        if memo[i] != -1:
            return memo[i]
        
        max_len = 1
        for j in range(i):
            if arr[j] < arr[i]:
                max_len = max(max_len, 1 + lis_ending_at(j))
        
        memo[i] = max_len
        return max_len
    
    return max(lis_ending_at(i) for i in range(n))

# Example usage:
arr = [10, 22, 9, 33, 21, 50, 41, 60, 80]
print("Length of LIS:", lis_memoization(arr))

###############################

def lis_tabulation(arr):
    n = len(arr)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

# Example usage:
arr = [10, 22, 9, 33, 21, 50, 41, 60, 80]
print("Length of LIS:", lis_tabulation(arr))

###############################
###Binary Search Approach (Not DP)

from bisect import bisect_left

def lis_optimized(arr):
    lis = []
    for num in arr:
        pos = bisect_left(lis, num)
        if pos == len(lis):
            lis.append(num)
        else:
            lis[pos] = num
    return len(lis)

# Example usage:
arr = [10, 22, 9, 33, 21, 50, 41, 60, 80]
print("Length of LIS:", lis_optimized(arr))

###############################
