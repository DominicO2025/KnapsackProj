import argparse
from models.knapsack import Knapsack

parser = argparse.ArgumentParser()

parser.add_argument("input_file_number", 
                    type=int,
                    help="Number of the text files to read the knapsack data from.")

args = parser.parse_args()


capacity_file_name = f"p{args.input_file_number:02d}_c.txt"
values_file_name = f"p{args.input_file_number:02d}_v.txt"
weights_file_name = f"p{args.input_file_number:02d}_w.txt"

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
        # knapsack.items consists of tuples, (j, k), where j is the value
        # of the ith item and k is the weight of the ith item 
        knapsack.items.append((knapsack.values[i], knapsack.weights[i]))
          
except FileNotFoundError as e:
    print(f"Error: file not found: {e.filename}")
    exit(1)

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
    cur_weight = knapsack.capacity
    for i in range(len(knapsack.items), 0, -1):
        if (dp[i - 1][cur_weight] == dp[i][cur_weight]):
            continue

        cur_weight -= knapsack.weights[i - 1]
        optimal_subset.append(i)


    optimal_value = dp[len(knapsack.items)][knapsack.capacity]

    return (optimal_value, optimal_subset[::-1])

#This is the memory function implementation of the knapsack problem.
def dfs(i,j, knapsack, dp):
    if i <= 0 or j <= 0: #return 0 if out of bounds
        return 0, []

    if dp[i][j] is not None:
        return dp[i][j]

    #calling functions
    if (j < knapsack.weights[i - 1]):  # skip current if the weight of the current item is greater then capacity
        return dfs(i-1, j, knapsack, dp)

    #grabbing vals from recurrsion
    item_above, op_sub1 = dfs(i-1, j, knapsack, dp)
    item_previous, op_sub2 = dfs(i-1, j - knapsack.weights[i - 1], knapsack, dp)

    #Have to do if statement, to know which val to put into current element with correct optimal subset
    if (item_above > (item_previous + knapsack.values[i-1])):
        dp[i][j] = item_above
        return item_above, op_sub1

    dp[i][j] = item_previous + knapsack.values[i-1]

    return item_previous + knapsack.values[i-1], op_sub2 + [i]

def memory_function(knapsack):
    """
    Task 1a: Dynamic Programming (memory function) approach

    Returns a tuple (optimal_value, optimal_subset)
    """
    # Create an (items x Capacity) table
    dp = [[0] * (knapsack.capacity + 1) for _ in range(len(knapsack.items) + 1)]

    optimal_value, optimal_subset = dfs(len(knapsack.items), knapsack.capacity, knapsack, dp)

    return (optimal_value, optimal_subset)

def greedy_approach_with_sorting(knapsack):
    """
    Task 2a: Greedy approach using sorting

    Returns a tuple (optimal_value, optimal_subset)
    """

    value_to_weight = []

    def merge_sort(arr):
        """
        Sorts an array in place, in descending order, using merge sort.

        arr is an array of (item_number, ratio) tuples, where item_number is
                the item's 1-based index and ratio is its value/weight ratio.
                Tuples are compared on the ratio (arr[i][1]) only.
        """
        if len(arr) > 1:

            left = arr[:len(arr) // 2]
            right = arr[len(arr) // 2:]

            merge_sort(left)
            merge_sort(right)

            i, j, k = 0, 0, 0

            # Merge the subarrays
            while i < len(left) and j < len(right):
                if left[i][1] >= right[j][1]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1

                k += 1

            while i < len(left):
                arr[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                arr[k] = right[j]
                j += 1
                k += 1
 
    for i in range(len(knapsack.items)):
        item = knapsack.items[i]

        # Storing the item number and tuple will make it
        # easier to sort the value_to_weight array  
        item_to_ratio_tuple = (i + 1, item[0] / item[1])
        value_to_weight.append(item_to_ratio_tuple)

    merge_sort(value_to_weight)

    cur_weight = 0
    optimal_value = 0
    optimal_subset = []

    # Go through items from highest to lowest value/weight ratio
    for item_number, _ in value_to_weight:
        value, weight = knapsack.items[item_number - 1]

        # Stop at the first item that doesn't fit
        if cur_weight + weight > knapsack.capacity:
            break

        cur_weight += weight
        optimal_value += value
        optimal_subset.append(item_number)

    return (optimal_value, sorted(optimal_subset))

#Memory function implementation of the knapsack problem, but with a hash table instead of a 2D array.
def dfs_hash(i,j, knapsack, dp):
    if i <= 0 or j <= 0: #return 0 if out of bounds
        return 0, []

    #calling functions
    if (j < knapsack.weights[i - 1]):  # skip current if the weight of the current item is greater then capacity
        return dfs(i-1, j, knapsack, dp)

    #grabbing vals from recurrsion
    item_above, op_sub1 = dfs(i-1, j, knapsack, dp)
    item_previous, op_sub2 = dfs(i-1, j - knapsack.weights[i - 1], knapsack, dp)

    #Have to do if statement, to know which val to put into current element with correct optimal subset
    if (item_above > (item_previous + knapsack.values[i-1])):
        dp[i][j] = item_above
        return item_above, op_sub1

    dp[i][j] = item_previous + knapsack.values[i-1]

    return item_previous + knapsack.values[i-1], op_sub2 + [i]

def memory_function_hash(knapsack):
    """
    Task 1a: Dynamic Programming (memory function) approach, but using a hash table

    Returns a tuple (optimal_value, optimal_subset)
    """
    # replace with hash table implementation
    dp = set()

    optimal_value, optimal_subset = dfs_hash(len(knapsack.items), knapsack.capacity, knapsack, dp)

    return (optimal_value, optimal_subset)


#actual main function call
traditional_approach_results = traditional_approach(knapsack)
memory_function_results = memory_function(knapsack)
greedy_approach = greedy_approach_with_sorting(knapsack)

print(f"Knapsack capacity: {knapsack.capacity}. Total number of items = f{len(knapsack.items)}")
print()
print(f"(1a) Traditional Dynamic Programming Optimal value: {traditional_approach_results[0]}")
print(f"(1a) Traditional Dynamic Programming Optimal subset: {traditional_approach_results[1]}")
print("(1a) Traditional Dynamic Programming Total Basic Ops: TBD TODO DO THIS DON'T FORGET DO THIS DON'T FORGET PLZ")

print()
print(f"(1b) Memory Function Dynamic Programming Optimal value: {memory_function_results[0]}")
print(f"(1b) Memory Function Dynamic Programming Optimal subset: {memory_function_results[1]}")
print("(1b) Memory Function Dynamic Programming Total Basic Ops: TBD TODO DO THIS DON'T FORGET DO THIS DON'T FORGET PLZ")

print()
print(f"(2a) Greedy Approach Optimal value: {greedy_approach[0]}")
print(f"(2a) Greedy Approach Optimal subset: {greedy_approach[1]}")
print("(2a) Greedy Approach Total Basic Ops: TBD TODO DO THIS DON'T FORGET DO THIS DON'T FORGET PLZ")