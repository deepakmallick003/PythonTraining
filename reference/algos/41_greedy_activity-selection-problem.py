def activity_selection(start_times, end_times):
    n = len(start_times)
    
    # Combine activities with their times
    activities = [(start_times[i], end_times[i]) for i in range(n)]
    
    # Sort by finish time
    activities.sort(key=lambda x: x[1])
    
    # The first activity always gets selected
    selected_activities = [activities[0]]
    
    # Iterate through activities and select the next non-overlapping one
    for i in range(1, n):
        if activities[i][0] >= selected_activities[-1][1]:
            selected_activities.append(activities[i])
    
    return selected_activities

# Example usage:
start_times = [1, 3, 0, 5, 8, 5]
end_times = [2, 4, 6, 7, 9, 9]

selected = activity_selection(start_times, end_times)
print("Selected activities:", selected)
