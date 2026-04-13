# Function to find modulo inverse of a with respect to m using extended Euclid's Algorithm
def modInverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

# Function implementing Chinese Remainder Theorem
def findMinX(num, rem, k):
    N = 1
    for i in range(k):
        N *= num[i]

    result = 0
    for i in range(k):
        n_i = N // num[i]
        inv_i = modInverse(n_i, num[i])
        result += rem[i] * n_i * inv_i

    return result % N

# Example usage
num = [3, 4, 5]
rem = [2, 3, 1]
k = len(num)
print("x is", findMinX(num, rem, k))  # Output: x is 11
