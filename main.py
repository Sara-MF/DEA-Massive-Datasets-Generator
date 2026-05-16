import pandas as pd
import random

from dea_ccr_output_oriented_pulp import dea_ccr_output_pulp
from dea_ccr_output_oriented_scipy import dea_ccr_output_scipy

qtd_dmus = 10

csv_name = "dataset_dea.csv"

data = []

for i in range(qtd_dmus):

    dmu = f"DMU_{i+1}"

    input_value = random.randint(1, 20)

    output_value = random.randint(1, 30)

    data.append([
        dmu,
        input_value,
        output_value
    ])

dataset = pd.DataFrame(
    data,
    columns=[
        "DMU",
        "Input",
        "Output"
    ]
)

dataset.to_csv(csv_name, index=False)
print("\nGENERATED DATASET\n")
print(dataset.to_string(index=False))

resultado_pulp = dea_ccr_output_pulp(csv_name)
print("\n\nRESULT DEA - PULP\n")
print(resultado_pulp.to_string(index=False))

resultado_scipy = dea_ccr_output_scipy(csv_name)
print("\n\nRESULT DEA - SCIPY\n")
print(resultado_scipy.to_string(index=False))