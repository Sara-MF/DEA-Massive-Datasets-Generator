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

while num_dmus < 3 * (num_inputs + num_outputs):

    print("\nThe inputs does not follow the rule:")
    print("num_dmus >= 3 * (num_inputs + num_outputs)\n")
    print("Insert the values again, respecting the rule\n")

    num_inputs = int(input("Insert the number of inputs: "))
    num_outputs = int(input("Insert the number of outputs: "))
    num_dmus = int(input("Insert the number of DMUs: "))

print("\nDEA CONFIGURATION\n")
print(f"DMUs: {num_dmus}")
print(f"Inputs: {num_inputs}")
print(f"Outputs: {num_outputs}")

data = []

global_weights = [
    random.uniform(0.8, 1.2)
    for _ in range(num_inputs)
]

for i in range(num_dmus):

    row = []

    # DMU name
    row.append(f"DMU_{i + 1}")

    # Creates correlation among all variables
    size_factor = random.uniform(100, 1000)

    inputs = []

    # Generate correlated inputs
    for j in range(num_inputs):
        input_value = (size_factor * random.uniform(0.90, 1.10))

        input_value = round(input_value)

        inputs.append(input_value)
        row.append(input_value)

    if random.random() < 0.03:
        true_efficiency = 1.0
    else:
        true_efficiency = random.triangular(
            0.40,
            0.95,
            0.65
        )

    productive_capacity = sum(
        w * x
        for w, x in zip(global_weights, inputs)
    )

    # Generate correlated outputs
    for j in range(num_outputs):
        output_factor = random.uniform(
            0.98,
            1.02
        )

        noise = random.uniform(
            0.995,
            1.005
        )

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
    columns.append(
        f"Input_{i + 1}"
    )

# Output columns
for i in range(num_outputs):
    columns.append(
        f"Output_{i + 1}"
    )

dataset = pd.DataFrame(data, columns=columns)

dataset.to_csv(csv_name, index=False)

print("\n----------------------")
print("\nGENERATED DATASET\n")
print(dataset.head(10))
print("\n----------------------\n")

result_pulp, efficients_ccr_output_pulp, inefficients_ccr_output_pulp = dea_ccr_output_pulp(csv_name)
print("RESULT DEA - CCR OUTPUT ORIENTED PULP\n")
print("Efficients:", efficients_ccr_output_pulp)
print("Inefficients:", inefficients_ccr_output_pulp)
print("\n----------------------\n")

result_pulp, efficients_ccr_input_pulp, inefficients_ccr_input_pulp = dea_ccr_input_pulp(csv_name)
print("RESULT DEA - CCR INPUT ORIENTED PULP\n")
print("Efficients:", efficients_ccr_input_pulp)
print("Inefficients:", inefficients_ccr_input_pulp)
print("\n----------------------\n")

result_pulp, efficients_bcc_output_pulp, inefficients_bcc_output_pulp = dea_bcc_output_pulp(csv_name)
print("RESULT DEA - BCC OUTPUT ORIENTED PULP\n")
print("Efficients:", efficients_bcc_output_pulp)
print("Inefficients:", inefficients_bcc_output_pulp)
print("\n----------------------\n")

result_pulp, efficients_bcc_input_pulp, inefficients_bcc_input_pulp = dea_bcc_input_pulp(csv_name)
print("RESULT DEA - BCC INPUT ORIENTED PULP\n")
print("Efficients:", efficients_bcc_input_pulp)
print("Inefficients:", inefficients_bcc_input_pulp)
print("\n----------------------\n")

result_scipy, efficients_ccr_output_scipy, inefficients_ccr_output_scipy = dea_ccr_output_scipy(csv_name)
print("RESULT DEA - CCR OUTPUT ORIENTED SCIPY\n")
print("Efficients:", efficients_ccr_output_scipy)
print("Inefficients:", inefficients_ccr_output_scipy)
print("\n----------------------\n")

result_scipy, efficients_ccr_input_scipy, inefficients_ccr_input_scipy = dea_ccr_input_scipy(csv_name)
print("RESULT DEA - CCR INPUT ORIENTED SCIPY\n")
print("Efficients:", efficients_ccr_input_scipy)
print("Inefficients:", inefficients_ccr_input_scipy)
print("\n----------------------\n")

result_scipy, efficients_bcc_output_scipy, inefficients_bcc_output_scipy = dea_bcc_output_scipy(csv_name)
print("RESULT DEA - BCC OUTPUT ORIENTED SCIPY\n")
print("Efficients:", efficients_bcc_output_scipy)
print("Inefficients:", inefficients_bcc_output_scipy)
print("\n----------------------\n")

result_scipy, efficients_bcc_input_scipy, inefficients_bcc_input_scipy = dea_bcc_input_scipy(csv_name)
print("RESULT DEA - BCC INPUT ORIENTED SCIPY\n")
print("Efficients:", efficients_bcc_input_scipy)
print("Inefficients:", inefficients_bcc_input_scipy)
print("\n")
