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
