import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor

csv_name = "dataset_dea.csv"

dataset = pd.read_csv(csv_name)

input_columns = [
    c for c in dataset.columns
    if c.startswith("Input")
]

output_columns = [
    c for c in dataset.columns
    if c.startswith("Output")
]

def calculate_vif(df):
    vif = pd.DataFrame()

    vif["Variable"] = df.columns

    vif["VIF"] = [
        variance_inflation_factor(df.values, i)
        for i in range(df.shape[1])
    ]

    return vif

vif_inputs = calculate_vif(
    dataset[input_columns]
)

vif_outputs = calculate_vif(
    dataset[output_columns]
)

print("\n")
print("VIF - INPUTS\n")
print(vif_inputs)

print("\n")
print("=" * 80)

print("\n")
print("VIF - OUTPUTS\n")
print(vif_outputs) 