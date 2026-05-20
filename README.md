# DEA Massive Datasets Generator

This project contains a generator of massive DEA datasets, which include a large number of inputs and outputs, as well as a large number of DMUs (Decision-Making Units).

## CCR Output Oriented

#### It was built two DEA solvers to compare results:
- DEA implemented with PuLp
- DEA implemented with SciPy

#### The solvers are being executed in a main file

## Main File

#### Generates a DEA dataset, with random numbers to inputs and outputs and then generate the number of DMUs respecting the rule:

` n >= max{m * s, 3(m + s)} `

`n = DMUs `

`m = inputs `

`s = outputs `

#### The dataset is export in csv format and is used by the solvers

#### Results are printed to be compared