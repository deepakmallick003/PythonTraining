# Rabin-Karp Algorithm Implementation

# A prime number for modulus
prime = 101

def rabin_karp(pattern, text):
    n = len(text)
    m = len(pattern)
    p_hash = 0  # Hash value for the pattern
    t_hash = 0  # Hash value for the current text window
    base = 256  # Number of characters in the input alphabet
    h = 1  # The value of base^(m-1)

    # Compute h = pow(base, m-1) % prime
    for i in range(m - 1):
        h = (h * base) % prime

    # Calculate the hash value of the pattern and the first window of the text
    for i in range(m):
        p_hash = (base * p_hash + ord(pattern[i])) % prime
        t_hash = (base * t_hash + ord(text[i])) % prime

    # Slide the pattern over text one by one
    for i in range(n - m + 1):
        # Check the hash values of the current window and the pattern
        if p_hash == t_hash:
            # Check for characters one by one
            if text[i:i + m] == pattern:
                print(f"Pattern found at index {i}")

        # Calculate the hash value for the next window of text
        if i < n - m:
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % prime

            # We might get a negative value of t_hash, converting it to positive
            if t_hash < 0:
                t_hash += prime

# Example usage
text = "ababcab"
pattern = "abc"
rabin_karp(pattern, text)
