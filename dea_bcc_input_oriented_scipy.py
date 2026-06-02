import pandas as pd
from scipy.optimize import linprog

def dea_bcc_input_scipy(csv_path):

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

        # linprog solves minimization problems.
        # In the BCC input-oriented DEA model the objective is to minimize theta.
        # [0]*n creates coefficients for lambdas and [1] creates the coefficient for theta.
        # The objective function will be min(0λ1 + 0λ2 + ... + 0λn + 1θ)
        objective_function = [0] * n + [1]

        # Matrix containing inequality constraint coefficients.
        # linprog uses the format: A_ub * x <= b_ub
        constraint_matrix = []

        # Vector containing the constrait limits.
        constraint_limits = []

        # Input constraints
        # DEA form:
        # Σ(λ_j * x_jk) ≤ θ * x_ik
        # Moving everything to the left side:
        # Σ(λ_j * x_jk) - θ*x_ik ≤ 0
        for input_col in input_columns:

            input_constraint = (
                list(dataset[input_col])
                + [-dataset.loc[i, input_col]]
            )

            constraint_matrix.append(
                input_constraint
            )

            constraint_limits.append(0)

        # Output constraints
        # DEA form:
        # Σ(λ_j * y_jr) ≥ y_ir
        # linprog requires constraints in <= format, so the equation is multiplied by -1:
        # -Σ(λ_j * y_jr) ≤ -y_ir
        for output_col in output_columns:

            output_constraint = (
                list(-dataset[output_col])
                + [0]
            )

            constraint_matrix.append(
                output_constraint
            )

            constraint_limits.append(
                -dataset.loc[i, output_col]
            )

        # BCC convexity constraint
        # Σ λ_j = 1
        # The theta coefficient is zero because theta does not participate in this equation.
        equality_matrix = [
            [1] * n + [0]
        ]

        equality_limits = [1]

        # Defines:
        # λj >= 0
        # θ >= 0
        # Total variables: n lambdas + 1 theta
        bounds = [(0, None)] * (n + 1)

        # Solves the DEA linear programming problem
        optimization_result = linprog(
            c=objective_function,
            A_ub=constraint_matrix,
            b_ub=constraint_limits,
            A_eq=equality_matrix,
            b_eq=equality_limits,
            bounds=bounds,
            method='highs'
        )

        # The last variable corresponds to theta
        if optimization_result.success:

            theta = optimization_result.x[-1]

            # In input-oriented DEA models efficiency is equal to theta
            efficiency = theta

            # Rounding reduces floating-point precision issues
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