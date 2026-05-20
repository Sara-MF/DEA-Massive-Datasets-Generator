import pandas as pd
from pulp import *

def dea_ccr_output_pulp(csv_path):

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

    for i in range(len(dataset)):

        dmu_name = dataset.loc[i, 'DMU']
        # input_dmu = dataset.loc[i, 'Input']
        # output_dmu = dataset.loc[i, 'Output']

        # Creates a linear programming problem using maximization,
        # since the CCR output-oriented model aims to maximize φ
        dea_model = LpProblem(f"DEA_CCR_Output_{dmu_name}", LpMaximize)

        # Constraint: φ ≥ 0
        phi = LpVariable("phi", lowBound=0)

        # Creates the λ_j variables associated with each reference DMU
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


        # Solves the linear programming problem using the CBC solver
        dea_model.solve(PULP_CBC_CMD(msg=0))

        phi_value = value(phi)

        # Avoid division by zero
        if phi_value is None or phi_value == 0:
            efficiency = 0
        else:
            # In output-oriented DEA models efficiency is calculated as 1/φ
            efficiency = 1 / phi_value

        # Rounding to 4 decimal places reduces floating-point precision issues
        status = (
            "Efficient"
            if round(efficiency, 4) >= 0.9999
            else "Inefficient"
        )

        result_row = {
            "DMU": dmu_name,
            "Phi": round(phi_value, 4),
            "Efficiency": round(efficiency, 4),
            "Status": status
        }

        results.append(result_row)

    result_dataset = pd.DataFrame(results)

    return result_dataset