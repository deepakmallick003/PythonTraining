def sieve_of_eratosthenes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    p = 2
    while p * p <= n:
        if is_prime[p]:
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1

    primes = [p for p in range(n + 1) if is_prime[p]]
    return primes

# Example usage:
n = 30
print(f"Prime numbers up to {n}: {sieve_of_eratosthenes(n)}")