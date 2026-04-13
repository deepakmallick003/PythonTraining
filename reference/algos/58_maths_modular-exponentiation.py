def modular_exponentiation(a, n, m):
    if n == 0:
        return 1
    elif n % 2 == 0:
        res = modular_exponentiation(a, n // 2, m)
        return (res * res) % m
    else:
        return ((a % m) * (modular_exponentiation(a, n - 1, m))) % m

# Example usage:
a = 7
n = 8
m = 9
result = modular_exponentiation(a, n, m)
print(result)  # Output: 4
