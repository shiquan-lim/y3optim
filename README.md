#Y3 Technologies Optimisation App

- clone repo
- navigate to project folder in terminal
- ensure local python runtime is >= v3.5
- run `pip install -t app/lib -r requirements.txt`. Currently, this will install DoCplex, the intermediary library for interacting with the CPLEX optimisation engine, and SciPy, a python machine learning library


# Launching anaconda environment / notebook
- Install anaconda3.6 from https://www.continuum.io/downloads
- via Terminal/ or anaconda Terminal, go to the directory where environment.yml is located at.
- ```conda env create -f environment.yml``` to create the environment.
- ```source activate y3optim``` (for mac) or ```activate y3optim``` (for windows) to activate the environment.
