def radix_sort(arr):
    # Print the original array
    print("Original array:", arr)

    # Initialize radixArray with 10 distinct empty lists for digits 0 to 9
    radixArray = [[] for _ in range(10)]

    # Find the maximum value in the array to determine the number of digits
    maxVal = max(arr)

    # Set the initial exponent to 1 (for the least significant digit)
    exp = 1

    # Loop until the exponent exceeds the maximum value
    while maxVal // exp > 0:

        # Distribute elements into buckets based on the current digit
        while len(arr) > 0:
            # Remove the last element from arr
            val = arr.pop()
            # Find the digit at the current exponent place
            radixIndex = (val // exp) % 10
            # Append the element to the corresponding bucket
            radixArray[radixIndex].append(val)

        # Collect elements back into arr from the buckets
        for bucket in radixArray:
            while len(bucket) > 0:
                # Remove the first element from the bucket
                val = bucket.pop(0)
                # Append the element back to arr
                arr.append(val)

        # Move to the next digit place
        exp *= 10

    # Print the sorted array
    print("Sorted array:", arr)


# Example usage
arr = [170, 45, 75, 90, 802, 24, 2, 66]
radix_sort(arr)
