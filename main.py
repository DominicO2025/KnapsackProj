import argparse
from models.knapsack import Knapsack

parser = argparse.ArgumentParser()

parser.add_argument("input_file_number",
                    help="Number of the text files to read the knapsack data from.")

args = parser.parse_args()


capacity_file_name = f"p0{args.input_file_number}_c.txt"
values_file_name = f"p0{args.input_file_number}_v.txt"
weights_file_name = f"p0{args.input_file_number}_w.txt"

knapsack = Knapsack()

try:
    with open(f"./data/{capacity_file_name}") as file:
        capacity = file.readline().strip()
        knapsack.capacity = int(capacity)

    with open(f"./data/{values_file_name}") as file:
        for line in file:
            value = line.strip()
            if value != "":
                knapsack.values.append(int(value))

    with open(f"./data/{weights_file_name}") as file:
        for line in file:
            weight = line.strip()
            if weight != "":
                knapsack.weights.append(int(weight))

    for i in range(len(knapsack.weights)):
        knapsack.items.append((knapsack.values[i], knapsack.weights[i]))
          
except FileNotFoundError as e:
    print(f"Error: file not found: {e.filename}")
    exit(1)

print("Capacity:", knapsack.capacity)
print("Values:", knapsack.values)
print("Weights:", knapsack.weights)
print("Items:", knapsack.items)

print()
def traditional_approach(knapsack):
    """
    Task 1a: Dynamic Programming (traditional) approach

    Returns a tuple (optimal_value, optimal_subset)
    """
    # Create an (items x Capacity) table
    dp = [[0] * (knapsack.capacity + 1) for _ in range(len(knapsack.items) + 1)]

    # Fill the table
    for i in range(1, len(knapsack.items) + 1):
        cur_weight = knapsack.weights[i - 1]
        cur_val = knapsack.values[i - 1]

        for j in range(1, knapsack.capacity + 1):
            skip = dp[i - 1][j]

            # If the weight of this item is > than the 
            # current capacity we can't take it
            if cur_weight > j:
                dp[i][j] = skip
                continue

            take = cur_val + dp[i - 1][j - cur_weight]
            dp[i][j] = max(skip, take)

    optimal_subset = []

    # Backtrack to get optimal subset
    # TODO

    optimal_value = dp[len(knapsack.items)][knapsack.capacity]

    return (optimal_value, optimal_subset)

optimal_results = traditional_approach(knapsack)
print("Optimal Results:", optimal_results)