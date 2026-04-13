def findPlatform(arrivals, departures):
    n = len(arrivals)
    
    # Sort arrival and departure times
    arrivals.sort()
    departures.sort()
    
    # platform_needed indicates number of platforms needed at a time
    platform_needed = 0
    max_platforms = 0
    i = 0
    j = 0
    
    # Use two pointers to traverse both arrays
    while i < n and j < n:
        # If the next event is an arrival, increment the number of platforms needed
        if arrivals[i] < departures[j]:
            platform_needed += 1
            i += 1
            # Update the maximum platforms needed
            max_platforms = max(max_platforms, platform_needed)
        else:
            # If the next event is a departure, decrease the platform count
            platform_needed -= 1
            j += 1
    
    return max_platforms

# Example usage
arrivals = [900, 940, 950, 1100, 1500, 1800]
departures = [910, 1200, 1120, 1130, 1900, 2000]
print("Minimum Number of Platforms Required =", findPlatform(arrivals, departures))
