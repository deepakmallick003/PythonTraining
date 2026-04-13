def knapsack_brute_force(weights, profits, capacity, n):
    # Base Case
    if n == 0 or capacity == 0:
        return 0

    # Recursive Case: Exclude or Include fractions
    if weights[n-1] > capacity:
        return knapsack_brute_force(weights, profits, capacity, n-1)
    else:
        include_item = profits[n-1] + knapsack_brute_force(weights, profits, capacity - weights[n-1], n-1)
        exclude_item = knapsack_brute_force(weights, profits, capacity, n-1)
        return max(include_item, exclude_item)

# Example Usage
weights = [9, 4, 5, 3]
profits = [90, 60, 100, 45]
capacity = 15

max_profit = knapsack_brute_force(weights, profits, capacity, len(weights))
print(f"Maximum profit with brute force approach: {max_profit}")


#############

class Fruit:
    def __init__(self, weight, profit):
        self.weight = weight
        self.profit = profit
        self.value_per_kg = profit / weight

def fractional_knapsack(fruits, capacity):
    # Sort fruits by their value per kg in decreasing order
    fruits.sort(key=lambda fruit: fruit.value_per_kg, reverse=True)

    total_profit = 0
    for fruit in fruits:
        if capacity >= fruit.weight:
            capacity -= fruit.weight
            total_profit += fruit.profit
        else:
            total_profit += fruit.value_per_kg * capacity
            break
    return total_profit

# Example Usage
fruits = [
    Fruit(9, 90),  # Avocado
    Fruit(4, 60),  # Mango
    Fruit(5, 100), # Banana
    Fruit(3, 45)   # Grapes
]
capacity = 15
max_profit = fractional_knapsack(fruits, capacity)
print(f"Maximum profit with greedy approach: {max_profit}")
