import pandas as pd
from pulp import *

def dea_ccr_input_pulp(csv_path):

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

        # Creates a linear programming problem using minimization,
        # since the CCR input-oriented model aims to minimize θ
        dea_model = LpProblem(f"DEA_CCR_Input_{dmu_name}", LpMinimize)

        # Decision variable:
        # θ >= 0
        theta = LpVariable("theta", lowBound=0)

        # Creates the λ_j variables associated with each reference DMU in the efficiency frontier
        # Constraint: λ_j >= 0
        lambdas = LpVariable.dicts(
            "lambda",
            range(len(dataset)),
            lowBound=0
        )

        # Objective function: minimize θ
        dea_model += theta

        # Input constraints
        # For each input k:
        # Σ(λ_j * x_jk) ≤ θ * x_ik
        for input_col in input_columns:
            dea_model += lpSum(
                lambdas[j] * dataset.loc[j, input_col]
                for j in range(len(dataset))
            ) <= theta * dataset.loc[i, input_col]

        # Output constraints
        # For each output r:
        # Σ(λ_j * y_jr) ≥ y_ir
        for output_col in output_columns:
            dea_model += lpSum(
                lambdas[j] * dataset.loc[j, output_col]
                for j in range(len(dataset))
            ) >= dataset.loc[i, output_col]

        # Solves the linear programming problem using the CBC solver
        dea_model.solve(PULP_CBC_CMD(msg=0))

        theta_value = value(theta)

        # Handles invalid solutions
        if theta_value is None:
            efficiency = 0
        else:
            # In input-oriented DEA, efficiency is directly equal to θ
            efficiency = theta_value

        # Rounding to 4 decimal places reduces floating-point precision issues
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
            "Theta": round(theta_value, 4),
            "Efficiency": round(efficiency, 4),
            "Status": status
        }

        results.append(result_row)

    result_dataset = pd.DataFrame(results)

    return result_dataset, efficients, inefficients