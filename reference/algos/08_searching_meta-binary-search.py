def meta_binary_search(arr, key):
    n = len(arr)
    if n == 0:
        return -1

    left, right = 0, n - 1
    bit = 1 << (right.bit_length() - 1)  # Start with the highest bit

    while bit > 0:
        mid = left + bit
        if mid < n and arr[mid] <= key:
            left = mid
        bit >>= 1  # Reduce the bit value

    if arr[left] == key:
        return left
    else:
        return -1

# Example usage
arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
key = 13
index = meta_binary_search(arr, key)
print(f"Element {key} is at index {index}")
