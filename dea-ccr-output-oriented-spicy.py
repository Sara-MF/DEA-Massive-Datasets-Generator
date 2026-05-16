import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import linprog

dataset = pd.DataFrame({
    'DMU':    ['A','B','C','D','E','F','G','H','I','J'],
    'Input':  [2,3,4,5,6,7,8,9,10,11],
    'Output': [4,6,8,9,11,13,14,16,18,20]
})

results = []

for i in range(len(dataset)):

    dmu_name = dataset.loc[i, 'DMU']
    current_input = dataset.loc[i, 'Input']
    current_output = dataset.loc[i, 'Output']

    n = len(dataset)

    # linprog solves only minimization problems.
    # Since the CCR output-oriented DEA model maximizes phi, the problem is converted to min(-phi).
    # [0]*n creates 0 coefficients for the lambdas and [-1] adds the coefficient for phi.
    # The objective function will be min(0λ1 + 0λ2 + ... + 0λn - 1φ)
    objective_function = [0]*n + [-1]

    # Matrix containing the constraint coefficients.
    # linprog uses the format: A_ub * x <= b_ub
    constraint_matrix = []

    # Vector containing the constraint limits.
    constraint_limits = []

    # Input constraint:
    # Σ(λj * xj) <= x0
    # Phi does not participate in this constraint, so its coefficient is 0.
    input_constraint = list(dataset["Input"]) + [0]
    constraint_matrix.append(input_constraint)
    constraint_limits.append(current_input)

    # Output constraint:
    # Σ(λj * yj) >= φ * y0
    # SciPy requires constraints in <= format, so the equation is multiplied by -1:
    # -Σ(λj * yj) + φ*y0 <= 0
    output_constraint = list(-dataset["Output"]) + [current_output]
    constraint_matrix.append(output_constraint)
    constraint_limits.append(0)

    # Defines:
    # λj >= 0
    # φ >= 0
    # There are n lambdas + 1 phi
    # Total: (n+1) variables
    bounds = [(0, None)] * (n + 1)

    # Solves the DEA linear programming problem
    optimization_result = linprog(
        c=objective_function,
        A_ub=constraint_matrix,
        b_ub=constraint_limits,
        bounds=bounds,
        method='highs'
    )

    # The last element of the solution corresponds to phi
    if optimization_result.success:
        phi = optimization_result.x[-1]
    else:
        print(f"Error on DMU {dmu_name}")

    # In output-oriented DEA models efficiency is calculated as 1/φ
    efficiency = 1 / phi

    # Rounding to 4 decimal places reduces floating-point precision issues
    status = (
        "Efficient"
        if round(efficiency, 4) >= 0.9999
        else "Inefficient"
    )

    results.append([
        dmu_name,
        current_input,
        current_output,
        round(phi, 4),
        round(efficiency, 4),
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
    plt.text(row["Input"]+0.05, row["Output"]+0.05, row["DMU"])

ef = result_dataset[
    result_dataset["Status"] == "Efficient"
].sort_values("Input")

plt.plot(
    ef["Input"],
    ef["Output"],
    linestyle="--",
    linewidth=2
)

plt.xlabel("Input")
plt.ylabel("Output")
plt.title("DEA CCR Output Oriented")
plt.grid(True)
plt.show()