def ternary_search(arr, key):
    left, right = 0, len(arr) - 1

    while right >= left:
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3

        if arr[mid1] == key:
            return mid1
        if arr[mid2] == key:
            return mid2

        if key < arr[mid1]:
            right = mid1 - 1
        elif key > arr[mid2]:
            left = mid2 + 1
        else:
            left = mid1 + 1
            right = mid2 - 1

    return -1

# Example usage
arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
key = 13
index = ternary_search(arr, key)
print(f"Element {key} is at index {index}")
