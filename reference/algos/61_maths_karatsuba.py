def karatsuba(x, y):
    # Base case for recursion
    if x < 10 or y < 10:
        return x * y

    # Calculate the size of the numbers
    n = max(len(str(x)), len(str(y)))
    m = n // 2

    # Split the digit sequences in the middle
    high1, low1 = divmod(x, 10**m)
    high2, low2 = divmod(y, 10**m)

    # Recursively calculate three products
    z0 = karatsuba(low1, low2)
    z1 = karatsuba((low1 + high1), (low2 + high2))
    z2 = karatsuba(high1, high2)

    return (z2 * 10**(2*m)) + ((z1 - z2 - z0) * 10**m) + z0

# Example usage:
x = 1234
y = 5678
result = karatsuba(x, y)
print(f"Product of {x} and {y} is {result}")
