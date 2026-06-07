# DEA Massive Dataset Generator

A Python-based academic project for generating large-scale synthetic datasets and evaluating Decision Making Units (DMUs) using Data Envelopment Analysis (DEA).

The project focuses on implementing and testing DEA models under different orientations and optimization libraries, allowing performance and consistency comparisons across solvers.

---

## Objectives

- Generate synthetic DEA datasets

- Implement classical DEA models:
  - CCR Input-Oriented
  - CCR Output-Oriented
  - BCC Input-Oriented
  - BCC Output-Oriented

- Compare optimization approaches using:
  - PuLP + CBC Solver
  - SciPy + HiGHS Solver

- Analyze efficiency classifications and solver behavior on large datasets.

---

## Features

- Automatic synthetic dataset generation
- Support for massive DEA datasets
- CCR and BCC DEA models
- Input-oriented and output-oriented formulations
- Implementations using both PuLP and SciPy
- Automatic efficiency classification
- Comparison between optimization libraries

---

## Project Structure

```text
.
├── main.py
│
├── dea_ccr_input_oriented_pulp.py
├── dea_ccr_output_oriented_pulp.py
│
├── dea_ccr_input_oriented_scipy.py
├── dea_ccr_output_oriented_scipy.py
│
├── dea_bcc_input_oriented_pulp.py
├── dea_bcc_output_oriented_pulp.py
│
├── dea_bcc_input_oriented_scipy.py
├── dea_bcc_output_oriented_scipy.py
│
└── dataset_dea.csv
```

---

## Dataset Generation

The dataset generator creates synthetic DEA datasets with realistic variability among DMUs.

### Dataset Characteristics

- User inserts the number of inputs, outputs and DMUs
- Random input values
- Controlled proportion of efficient DMUs
- Output values generated from production capacity estimates
- Random noise to increase variability

Rule for the number of inputs, outputs and DMUs:

```python
num_dmus >= 3 * (num_inputs + num_outputs)
```

Generated dataset format:

```text
DMU | Input_1 | Input_2 | ... | Output_1 | Output_2 | ...
```

---
## Optimization Libraries

### PuLP Implementation

Library:

```python
from pulp import *
```

Solver:

```text
CBC (Coin-or Branch and Cut)
```

Characteristics:

- Algebraic modeling approach
- Easy-to-read mathematical formulation
- Suitable for educational and research purposes

---

### SciPy Implementation

Library:

```python
from scipy.optimize import linprog
```

Solver:

```text
HiGHS
```

Characteristics:

- Matrix-based formulation
- Efficient for large-scale linear programming problems
- Lower-level implementation with reduced modeling overhead

---

## Output

Each DEA model returns a dataset containing:

| Column | Description |
|----------|------------|
| DMU | Decision Making Unit |
| Efficiency | Efficiency score |
| Status | Efficient or Inefficient |

Example:

```text
DMU      Efficiency   Status
DMU_1    1.0000       Efficient
DMU_2    0.8734       Inefficient
DMU_3    1.0000       Efficient
```

Summary statistics are also reported:

```text
Total Efficient DMUs
Total Inefficient DMUs
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Sara-MF/DEA-Massive-Datasets-Generator.git
```

Install dependencies:

```bash
pip install pandas scipy pulp
```

---

## Usage

Run:

```bash
python main.py
```

The script will:

1. Wait user inserts the number of inputs, outputs and DMUs
2. Generate a synthetic DEA dataset
3. Save the dataset as `dataset_dea.csv`
4. Execute all CCR and BCC DEA models
5. Create a csv file for each model to store results
6. Display efficiency statistics for each implementation

---

## Technologies

- Python 3.11.9
- Pandas
- PuLP
- SciPy
- CBC Solver
- HiGHS Solver