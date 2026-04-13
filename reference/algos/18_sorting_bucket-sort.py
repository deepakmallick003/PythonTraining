def insertion_sort(bucket):
    # Simple insertion sort to sort individual buckets
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        while j >= 0 and key < bucket[j]:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = key
    return bucket

def bucket_sort(arr):
    if len(arr) == 0:
        return arr

    # Print the original array
    print("Original array:", arr)

    # Find maximum value in the array to know the range
    max_val = max(arr)
    size = max_val / len(arr)

    # Create empty buckets
    buckets = [[] for _ in range(len(arr))]

    # Distribute elements into buckets
    for i in range(len(arr)):
        j = int(arr[i] / size)
        if j != len(arr):
            buckets[j].append(arr[i])
        else:
            buckets[len(arr) - 1].append(arr[i])

    # Sort each bucket and concatenate the result
    sorted_array = []
    for i in range(len(arr)):
        sorted_array.extend(insertion_sort(buckets[i]))

    # Print the sorted array
    print("Sorted array:", sorted_array)
    return sorted_array

# Example usage
arr = [170, 45, 75, 90, 802, 24, 2, 66]
bucket_sort(arr)
