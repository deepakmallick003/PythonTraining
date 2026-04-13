def pigeonhole_sort(arr):
    if len(arr) == 0:
        return arr

    # Find the minimum and maximum values in the array
    min_val = min(arr)
    max_val = max(arr)
    range_of_elements = max_val - min_val + 1

    # Initialize pigeonholes
    pigeonholes = [[] for _ in range(range_of_elements)]

    # Place elements into their respective pigeonholes
    for num in arr:
        pigeonholes[num - min_val].append(num)

    # Collect elements from the pigeonholes in order
    sorted_index = 0
    for i in range(range_of_elements):
        while len(pigeonholes[i]) > 0:
            arr[sorted_index] = pigeonholes[i].pop(0)
            sorted_index += 1

    return arr

# Example usage
arr = [8, 3, 2, 7, 4, 6, 8, 3, 5, 1]
print("Original array:", arr)
pigeonhole_sort(arr)
print("Sorted array:", arr)
