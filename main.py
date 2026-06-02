import pandas as pd
import random

from dea_ccr_output_oriented_pulp import dea_ccr_output_pulp
from dea_ccr_input_oriented_pulp import dea_ccr_input_pulp
from dea_bcc_output_oriented_pulp import dea_bcc_output_pulp
from dea_bcc_input_oriented_pulp import dea_bcc_input_pulp

from dea_ccr_output_oriented_scipy import dea_ccr_output_scipy
from dea_ccr_input_oriented_scipy import dea_ccr_input_scipy
from dea_bcc_output_oriented_scipy import dea_bcc_output_scipy
from dea_bcc_input_oriented_scipy import dea_bcc_input_scipy

csv_name = "dataset_dea.csv"

num_inputs = int(input("Insert the number of inputs: "))
num_outputs = int(input("Insert the number of outputs: "))
num_dmus = int(input("Insert the number of DMUs: "))

print("\nDEA CONFIGURATION\n")
print(f"DMUs: {num_dmus}")
print(f"Inputs: {num_inputs}")
print(f"Outputs: {num_outputs}")

data = []

for i in range(num_dmus):

    row = []

    # DMU name
    row.append(f"DMU_{i + 1}")

    inputs = []

    # Input values
    for j in range(num_inputs):
        input_value = random.randint(50, 1000)

        inputs.append(input_value)
        row.append(input_value)

   # Controls the proportion of efficient DMUs
    if random.random() < 0.08:
        true_efficiency = 1.0
    else:
        true_efficiency = random.uniform(
            0.50,
            0.95
        )

    # Assigns a relative importance to each input
    weights = [
        random.uniform(0.5, 1.5)
        for _ in range(num_inputs)
    ]

    # Estimates the DMU's production capacity
    productive_capacity = sum(
        w * x
        for w, x in zip(weights, inputs)
    )

    # Output values
    for j in range(num_outputs):

        # Introduces variation among outputs
        output_factor = random.uniform(
            0.6,
            1.3
        )

        # Introduces random variation
        noise = random.uniform(
            0.90,
            1.10
        )

        # Generates the final output value
        output_value = (
            productive_capacity
            * true_efficiency
            * output_factor
            * noise
        )

        row.append(
            round(output_value)
        )

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
print("\n----------------------\n\nGENERATED DATASET\n")
print(dataset.head())
print("\n----------------------\n")

result_pulp, efficients_ccr_output_pulp, inefficients_ccr_output_pulp = dea_ccr_output_pulp(csv_name)
print("RESULT DEA - CCR OUTPUT ORIENTED PULP\n")
# print(result_pulp.to_string(index=False))
print("Efficients: ", efficients_ccr_output_pulp)
print("Inefficients: ", inefficients_ccr_output_pulp)
print("\n----------------------\n")

result_pulp, efficients_ccr_input_pulp, inefficients_ccr_input_pulp = dea_ccr_input_pulp(csv_name)
print("RESULT DEA - CCR INPUT ORIENTED PULP\n")
# print(result_pulp.to_string(index=False))
print("Efficients: ", efficients_ccr_input_pulp)
print("Inefficients: ", inefficients_ccr_input_pulp)
print("\n----------------------\n")

result_pulp, efficients_bcc_output_pulp, inefficients_bcc_output_pulp = dea_bcc_output_pulp(csv_name)
print("RESULT DEA - BCC OUTPUT ORIENTED PULP\n")
# print(result_pulp.to_string(index=False))
print("Efficients: ", efficients_bcc_output_pulp)
print("Inefficients: ", inefficients_bcc_output_pulp)
print("\n----------------------\n")

result_pulp, efficients_bcc_input_pulp, inefficients_bcc_input_pulp = dea_bcc_input_pulp(csv_name)
print("RESULT DEA - BCC INPUT ORIENTED PULP\n")
# print(result_pulp.to_string(index=False))
print("Efficients: ", efficients_bcc_input_pulp)
print("Inefficients: ", inefficients_bcc_input_pulp)
print("\n----------------------\n")

result_scipy, efficients_ccr_output_scipy, inefficients_ccr_output_scipy = dea_ccr_output_scipy(csv_name)
print("RESULT DEA - CCR OUTPUT ORIENTED SCIPY\n")
# print(result_scipy.to_string(index=False))
print("Efficients: ", efficients_ccr_output_scipy)
print("Inefficients: ", inefficients_ccr_output_scipy)
print("\n----------------------\n")

result_scipy, efficients_ccr_input_scipy, inefficients_ccr_input_scipy = dea_ccr_input_scipy(csv_name)
print("RESULT DEA - CCR INPUT ORIENTED SCIPY\n")
# print(result_scipy.to_string(index=False))
print("Efficients: ", efficients_ccr_input_scipy)
print("Inefficients: ", inefficients_ccr_input_scipy)
print("\n----------------------\n")

result_scipy, efficients_bcc_output_scipy, inefficients_bcc_output_scipy = dea_bcc_output_scipy(csv_name)
print("RESULT DEA - BCC OUTPUT ORIENTED SCIPY\n")
# print(result_scipy.to_string(index=False))
print("Efficients: ", efficients_bcc_output_scipy)
print("Inefficients: ", inefficients_bcc_output_scipy)
print("\n----------------------\n")

result_scipy, efficients_bcc_input_scipy, inefficients_bcc_input_scipy = dea_bcc_input_scipy(csv_name)
print("RESULT DEA - BCC INPUT ORIENTED SCIPY\n")
# print(result_scipy.to_string(index=False))
print("Efficients: ", efficients_bcc_input_scipy)
print("Inefficients: ", inefficients_bcc_input_scipy)
print("\n")
