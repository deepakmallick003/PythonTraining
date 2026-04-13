def counting_sort(arr):
    size = len(arr)
    output = [0] * size

    # Initialize count array with zeros for the range of input values
    max_val = max(arr) + 1
    count = [0] * max_val

    # Store the count of each element in count array
    for i in range(0, size):
        count[arr[i]] += 1

    # Store the cumulative count
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # Place the elements in output array based on cumulative counts
    i = size - 1
    while i >= 0:
        output[count[arr[i]] - 1] = arr[i]
        count[arr[i]] -= 1
        i -= 1

    # Copy the sorted elements into the original array
    for i in range(0, size):
        arr[i] = output[i]

# Example usage
arr = [4, 2, 2, 8, 3, 3, 1]
counting_sort(arr)
print("Sorted array is:", arr)