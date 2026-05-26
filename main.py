import pandas as pd
import random

from dea_ccr_output_oriented_pulp import dea_ccr_output_pulp
from dea_ccr_output_oriented_scipy import dea_ccr_output_scipy

csv_name = "dataset_dea.csv"

# Generating random quantity of inputs and outputs
num_inputs = random.randint(2, 5)
num_outputs = random.randint(1, 3)

# DEA rule:
# n >= max{m*s, 3(m+s)}
#
# n = DMUs
# m = inputs
# s = outputs
min_dmus = max(num_inputs * num_outputs, 3 * (num_inputs + num_outputs))

# Generating random quantity of DMUs respecting the rule
num_dmus = max(min_dmus, min_dmus + 200)

print("\nDEA CONFIGURATION\n")
print(f"DMUs: {num_dmus}")
print(f"Inputs: {num_inputs}")
print(f"Outputs: {num_outputs}")

# Trying inserting weights
# weights = [
#     random.uniform(0.5, 2)
#     for _ in range(num_inputs)
# ]

data = []

for i in range(num_dmus):

    row = []

    # DMU name
    row.append(f"DMU_{i + 1}")

    inputs = []

    # Input values
    for j in range(num_inputs):
        input_value = random.randint(1, 20)

        inputs.append(input_value)
        row.append(input_value)

    total_inputs = sum(inputs)

    # Output values
    for j in range(num_outputs):
        # Random proportional factor
        if random.random() < 0.15:
            proportional_factor = random.uniform(
                0.98,
                1.05
            )
        else:
            proportional_factor = random.uniform(
                0.55,
                0.95
            )

        # Random noise
        noise = random.uniform(-10, 10)

        output_value = abs(int((total_inputs * proportional_factor) + noise))

        row.append(output_value)

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
# print("\nGENERATED DATASET\n")
# print(dataset.to_string(index=False))

result_pulp, efficients_pulp, inefficients_pulp = dea_ccr_output_pulp(csv_name)
print("\n\nRESULT DEA - PULP\n")
# print(result_pulp.to_string(index=False))
print("Efficients - PULP: ", efficients_pulp)
print("Inefficients - PULP: ", inefficients_pulp)

result_scipy, efficients_scipy, inefficients_scipy = dea_ccr_output_scipy(csv_name)
print("\n\nRESULT DEA - SCIPY\n")
# print(result_scipy.to_string(index=False))
print("Efficients - PULP: ", efficients_scipy)
print("Inefficients - PULP: ", inefficients_scipy)