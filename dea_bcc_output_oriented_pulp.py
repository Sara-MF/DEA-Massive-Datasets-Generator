import pandas as pd
from pulp import *

def dea_bcc_output_pulp(csv_path):

    dataset = pd.read_csv(csv_path)

    input_columns = [
        col for col in dataset.columns
        if col.startswith("Input_")
    ]

    output_columns = [
        col for col in dataset.columns
        if col.startswith("Output_")
    ]

    results = []

    efficients = 0

    inefficients = 0

    for i in range(len(dataset)):

        dmu_name = dataset.loc[i, 'DMU']

        # Creates the DEA model
        dea_model = LpProblem(f"DEA_BCC_Output_{dmu_name}", LpMaximize)

        # Constraint: φ ≥ 0
        phi = LpVariable("phi", lowBound=0)

        # Lambda variables
        lambdas = LpVariable.dicts(
            "lambda",
            range(len(dataset)),
            lowBound=0
        )

        # Objective function: maximize φ
        dea_model += phi

        # Input constraints
        # For each input k:
        # Σ(λ_j * x_jk) ≤ x_ik
        for input_col in input_columns:
            dea_model += lpSum(
                lambdas[j] * dataset.loc[j, input_col]
                for j in range(len(dataset))
            ) <= dataset.loc[i, input_col]

        # Output constraints
        # For each output r:
        # Σ(λ_j * y_jr) ≥ φ * y_ir
        for output_col in output_columns:
            dea_model += lpSum(
                lambdas[j] * dataset.loc[j, output_col]
                for j in range(len(dataset))
            ) >= phi * dataset.loc[i, output_col]

        # BCC convexity constraint
        dea_model += lpSum(
            lambdas[j]
            for j in range(len(dataset))
        ) == 1

        # Solves the LP problem
        dea_model.solve(PULP_CBC_CMD(msg=0))

        phi_value = value(phi)

        if phi_value is None or phi_value == 0:
            efficiency = 0
        else:
            efficiency = 1 / phi_value

        status = (
            "Efficient"
            if round(efficiency, 4) >= 0.9999
            else "Inefficient"
        )

        if status == "Efficient":
            efficients += 1
        else:
            inefficients += 1

        result_row = {
            "DMU": dmu_name,
            "Phi": round(phi_value, 4),
            "Efficiency": round(efficiency, 4),
            "Status": status
        }

        results.append(result_row)

    result_dataset = pd.DataFrame(results)

    return result_dataset, efficients, inefficients