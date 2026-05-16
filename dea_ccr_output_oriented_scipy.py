import pandas as pd
from scipy.optimize import linprog

def dea_ccr_output_scipy(csv_path):

    dataset = pd.read_csv(csv_path)

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

        else:
            results.append([
                dmu_name,
                current_input,
                current_output,
                None,
                None,
                "Optimization Error"
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

