def matrix_multiply(A, B):
    c = [[A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]]]

    return c

def matrix_power(M, n):
    if n == 0:
        return [[1, 0], [0, 1]]
    elif n == 1:
        return M
    elif n % 2 == 0:
        half_power = matrix_power(M, n // 2)
        return matrix_multiply(half_power, half_power)
    else:
        half_power = matrix_power(M, n // 2)
        return matrix_multiply(matrix_multiply(half_power, half_power), M)

def fib(n):
    if n == 0:
        return 0
    F = [[1, 1], [1, 0]]
    result = matrix_power(F, n - 1)
    return result[0][0]

# Example: Find the 10th Fibonacci number
print(fib(10))  # Output: 55
