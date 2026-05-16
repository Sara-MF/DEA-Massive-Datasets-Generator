import pandas as pd
from pulp import *

def dea_ccr_output_pulp(csv_path):

    dataset = pd.read_csv(csv_path)

    results = []

    for i in range(len(dataset)):

        dmu_name = dataset.loc[i, 'DMU']
        input_dmu = dataset.loc[i, 'Input']
        output_dmu = dataset.loc[i, 'Output']

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

        # Input constraint:
        # Σ(λ_j * x_j) ≤ x₀
        dea_model += lpSum(
            lambdas[j] * dataset.loc[j, 'Input']
            for j in range(len(dataset))
        ) <= input_dmu

        # Output constraint:
        # Σ(λ_j * y_j) ≥ φ * y₀
        dea_model += lpSum(
            lambdas[j] * dataset.loc[j, 'Output']
            for j in range(len(dataset))
        ) >= phi * output_dmu

        # Solves the linear programming problem using the CBC solver
        dea_model.solve(PULP_CBC_CMD(msg=0))

        # In output-oriented DEA models efficiency is calculated as 1/φ
        efficiency = 1 / value(phi)

        # Rounding to 4 decimal places reduces floating-point precision issues
        status = (
            "Efficient"
            if round(efficiency, 4) >= 0.9999
            else "Inefficient"
        )

        results.append([
            dmu_name,
            input_dmu,
            output_dmu,
            round(value(phi),4),
            round(efficiency,4),
            status
        ])

    result_dataset = pd.DataFrame(
        results,
        columns=[
            "DMU",
            "Input",
            "Output",
            "Phi",
            "Efficiency",
            "Status"
        ]
    )

    return result_dataset