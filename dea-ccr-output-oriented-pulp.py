import pandas as pd
import matplotlib.pyplot as plt
from pulp import *

dataset = pd.DataFrame({
    'DMU':    ['A','B','C','D','E','F','G','H','I','J'],
    'Input':  [2,3,4,5,6,7,8,9,10,11],
    'Output': [4,6,8,9,11,13,14,16,18,20]
})

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

print("\nRESULT DEA CCR OUTPUT ORIENTED\n")
print(result_dataset.to_string(index=False))

plt.figure(figsize=(8,6))

for _, row in result_dataset.iterrows():

    cor = "green" if row["Status"] == "Efficient" else "red"

    plt.scatter(row["Input"], row["Output"], color=cor, s=100)

    plt.text(row["Input"] + 0.05, row["Output"] + 0.05, row["DMU"])

graphic = result_dataset[
    result_dataset["Status"] == "Efficient"
].sort_values("Input")

plt.plot(
    graphic["Input"],
    graphic["Output"],
    linestyle="--",
    linewidth=2
)

plt.xlabel("Input")
plt.ylabel("Output")
plt.title("DEA CCR Output Oriented")

plt.grid(True)
plt.show()