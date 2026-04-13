def job_sequencing_greedy(jobs, profits, deadlines):
    # Step 1: Sort jobs based on profit in descending order
    jobs_with_profits = sorted(zip(jobs, profits, deadlines), key=lambda x: x[1], reverse=True)
    
    n = len(jobs)
    time_slots = [-1] * n  # Initialize time slots, -1 indicates empty
    total_profit = 0
    
    for job, profit, deadline in jobs_with_profits:
        # Find the latest time slot available for this job
        for t in range(min(n, deadline) - 1, -1, -1):
            if time_slots[t] == -1:  # Empty slot found
                time_slots[t] = job
                total_profit += profit
                break
    
    scheduled_jobs = [time_slots[i] for i in range(n) if time_slots[i] != -1]
    return scheduled_jobs, total_profit


jobs = ['J1', 'J2', 'J3', 'J4', 'J5']
profits = [100, 19, 27, 25, 15]
deadlines = [2, 1, 2, 1, 3]

scheduled_jobs, total_profit = job_sequencing_greedy(jobs, profits, deadlines)

print("Scheduled Jobs:", scheduled_jobs)
print("Total Profit:", total_profit)
