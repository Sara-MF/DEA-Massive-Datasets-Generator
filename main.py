import pandas as pd
import random

from dea_ccr_output_oriented_pulp import dea_ccr_output_pulp
from dea_ccr_output_oriented_scipy import dea_ccr_output_scipy

csv_name = "dataset_dea.csv"

# Generating random quantity of inputs and outputs
num_inputs = random.randint(10, 30)
num_outputs = random.randint(10, 20)

# DEA rule:
# n >= max{m*s, 3(m+s)}
#
# n = DMUs
# m = inputs
# s = outputs
min_dmus = max(num_inputs * num_outputs, 3 * (num_inputs + num_outputs))

# Generating random quantity of DMUs respecting the rule
num_dmus = random.randint(min_dmus, min_dmus + 20)

print("\nDEA CONFIGURATION\n")
print(f"DMUs: {num_dmus}")
print(f"Inputs: {num_inputs}")
print(f"Outputs: {num_outputs}")

data = []

for i in range(num_dmus):

    row = []

    # DMU name
    row.append(f"DMU_{i + 1}")

    # Input values
    for j in range(num_inputs):
        row.append(random.randint(1, 20))

    # Output values
    for j in range(num_outputs):
        row.append(random.randint(1, 30))

    data.append(row)

columns = ["DMU"]

# Input columns
for i in range(num_inputs):
    columns.append(f"Input_{i + 1}")

# Output columns
for i in range(num_outputs):
    columns.append(f"Output_{i + 1}")

dataset = pd.DataFrame(data, columns=columns)

dataset.to_csv(csv_name, index=False)
print("\nGENERATED DATASET\n")
print(dataset.to_string(index=False))

result_pulp = dea_ccr_output_pulp(csv_name)
print("\n\nRESULT DEA - PULP\n")
print(result_pulp.to_string(index=False))

result_scipy = dea_ccr_output_scipy(csv_name)
print("\n\nRESULT DEA - SCIPY\n")
print(result_scipy.to_string(index=False))