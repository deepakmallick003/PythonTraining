def sentinelLinearSearch(arr, targetVal):
    n = len(arr)
    arr.append(targetVal)  # Add the sentinel value at the end
    i = 0
    
    while arr[i] != targetVal:
        i += 1
    
    arr.pop()  # Remove the sentinel value

    if i < n:
        print(key, "is present at index", i)  # Found the target in the original array
    else:
        print("Element Not found")  # Target was not in the original array
 
 
# Driver code
arr = [10, 20, 180, 30, 60, 50, 110, 100, 70]
key = 180
 
sentinelLinearSearch(arr, key)