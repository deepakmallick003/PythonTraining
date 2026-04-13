
###############################

def coin_change_tabulation(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1

# Example usage:
coins = [5, 9]
amount = 12
print("Fewest coins needed:", coin_change_tabulation(coins, amount))

###############################