MIN_RUN = 32

def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge(arr, l, m, r):
    len1, len2 = m - l + 1, r - m
    left, right = [], []
    for i in range(0, len1):
        left.append(arr[l + i])
    for i in range(0, len2):
        right.append(arr[m + 1 + i])
    
    i, j, k = 0, 0, l
    
    while i < len1 and j < len2:
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    
    while i < len1:
        arr[k] = left[i]
        k += 1
        i += 1
    
    while j < len2:
        arr[k] = right[j]
        k += 1
        j += 1

def timsort(arr):
    n = len(arr)
    for i in range(0, n, MIN_RUN):
        insertion_sort(arr, i, min((i + MIN_RUN - 1), n - 1))
    
    size = MIN_RUN
    while size < n:
        for start in range(0, n, size * 2):
            mid = min((start + size - 1), n - 1)
            end = min((start + 2 * size - 1), n - 1)
            if mid < end:
                merge(arr, start, mid, end)
        size *= 2

# Example usage
arr = [170, 45, 75, 90, 802, 24, 2, 66]
timsort(arr)
print("Sorted array:", arr)
