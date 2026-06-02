import pandas as pd
from scipy.optimize import linprog

def dea_ccr_input_scipy(csv_path):

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

    n = len(dataset)

    for i in range(n):

        dmu_name = dataset.loc[i, 'DMU']

        # The CCR input-oriented DEA model minimizes theta.
        # linprog solves minimization problems directly.
        # [0]*n creates 0 coefficients for the lambdas and [1] adds the coefficient for theta.
        # The objective function will be: min(0λ1 + 0λ2 + ... + 0λn + 1θ)
        objective_function = [0] * n + [1]

        # Matrix containing the constraint coefficients.
        # linprog uses the format: A_ub * x <= b_ub
        constraint_matrix = []

        # Vector containing the constraint limits.
        constraint_limits = []

        # Input constraints
        # Original DEA form:
        # Σ(λ_j * x_jk) ≤ θ * x_ik
        #
        # Moving everything to the left side:
        # Σ(λ_j * x_jk) - θ*x_ik ≤ 0
        for input_col in input_columns:

            input_constraint = (
                list(dataset[input_col])
                + [-dataset.loc[i, input_col]]
            )

            constraint_matrix.append(input_constraint)

            constraint_limits.append(0)

        # Output constraints
        # Original DEA form:
        # Σ(λ_j * y_jr) ≥ y_ir
        #
        # linprog requires constraints in <= format,
        # so the equation is multiplied by -1:
        #
        # -Σ(λ_j * y_jr) ≤ -y_ir
        for output_col in output_columns:

            output_constraint = (
                list(-dataset[output_col])
                + [0]
            )

            constraint_matrix.append(output_constraint)

            constraint_limits.append(
                -dataset.loc[i, output_col]
            )

        # Defines:
        # λj >= 0
        # θ >= 0
        # There are n lambdas + 1 theta
        # Total: (n + 1) variables
        bounds = [(0, None)] * (n + 1)

        # Solves the DEA linear programming problem
        optimization_result = linprog(
            c=objective_function,
            A_ub=constraint_matrix,
            b_ub=constraint_limits,
            bounds=bounds,
            method='highs'
        )

        # The last element of the solution corresponds to theta
        if optimization_result.success:

            theta = optimization_result.x[-1]

            # In input-oriented DEA models efficiency is equal to theta
            efficiency = theta

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
                "Theta": round(theta, 4),
                "Efficiency": round(efficiency, 4),
                "Status": status
            }

        else:

            result_row = {
                "DMU": dmu_name,
                "Theta": None,
                "Efficiency": None,
                "Status": "Optimization Error"
            }

        results.append(result_row)

    result_dataset = pd.DataFrame(results)

    return result_dataset, efficients, inefficients