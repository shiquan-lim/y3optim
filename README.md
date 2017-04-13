# Introduction
This is an application created for [Y3 Technologies](http://www.y3technologies.com) built by [Lim Shi Quan](https://github.com/shiquan-lim), [Russell Yap](https://github.com/russellyap), [Gideon Raj]() and [Amos Tan](https://github.com/atwj) as a project for under the __IS421 – Enterprise Analytics for Decision Support__ elective by Singapore Management University, School Of Information Systems.

The purpose of this project is to design and build an application that takes in information about a customer (such as age and budget), will recommend a set of items that will maximize the customer's satisfaction.

# Installation
Here we provide three ways of setting up the application.
## #1 – Build from repository
1. Clone repository with `git clone https://github.com/shiquan-lim/y3optim.git`
2. Ensure local python runtime is >= v3.5
3. Navigate to project folder in terminal
4. Run `pip install -t app/lib -r requirements.txt`. 

## #2 - Build from environment.yml file
1. Install anaconda 3.6 from https://www.continuum.io/downloads
2. Clone repository with `git clone https://github.com/shiquan-lim/y3optim.git`
3. via Terminal/ or anaconda Terminal, go to the directory where environment.yml is located at.
4. Create the environment with `conda env create -f environment.yml`.
5. Activate the environment with `source activate y3optim` (for Mac) or ```activate y3optim``` (for Windows).

## #3 – Creating Exact environment using spec-file.txt (tested for mac only)
1. Install anaconda 3.6 from https://www.continuum.io/downloads
2. Clone repository with `git clone https://github.com/shiquan-lim/y3optim.git`
3. via Terminal/ or anaconda Terminal, go to the directory where environment.yml is located at.
4. Create the environment with `conda env create --name y3optim --file spec-file.txt`
5. Activate the environment with `source activate y3optim` (for Mac) or ```activate y3optim``` (for Windows).

# Usage

## main.py
`main.py` is a command line application. To use the application, we assume that the user has set up the database and run the `data.py` script that will load the tables required by the application. 

1. Using terminal or command prompt, go to the directory of the project and activate the python environment with `source activate y3optim` (for Mac) or ```activate y3optim``` (for Windows).
2. Start the application with `python main.py`. Follow the instructions returned by the program.
```
(anaconda3-4.2.0/envs/y3optim) Amoss-MacBook-Pro:app amos$ python main.py
Please enter: main.py [budget] [group size] [your age] [dietary restrictions (x,y,z)] [weather] [verbose (1/0)]
Welcome to the beta of YouFood 1.0,

developed by Marksmen2.0 for Y3technologies.

To use this application, please enter the following information

main.py [budget] [group size] [your age] [food preferences (x,y,z)] [weather] [verbose (1/0)]

Please adhere to this format.

Budget => allowable expenditure in dollars.

Group size => Number of diners

Age => Age in years

Food preferences can be any (0 - many) of the following categories

- Chicken

- Pork

- Seafood

- Fish

- Beef

- Vegetarian

If you have no preferences, you may simply enter "-".

Weather => Sunny or Rainy
```

## data.py
`data.py` is a utility script that takes in a `.csv` file containing the transaction data of customers at a given store. For this script to work we assume that the file is of similar format to that as [`data_final_v2.csv`](https://github.com/shiquan-lim/y3optim/blob/master/data/data_final_v2.csv)

1. Using your favorite text editor, change the database credentials (`dbname`,`user`,`pw`,`host` and `port`) to your own.
2. Change the `file` variable to the location of your input file.
3. Change the `outputpath` variable to the location where you want the output files to be.
4. Save the python file and close the text editor.
5. Go to script location, and activate the python environment with `source activate y3optim` (for Mac) or ```activate y3optim``` (for Windows).
6. Run the script with `python data.py`
7. You should see 96 tables and csv files in the database/directory specified in steps 1 and 3.

# Benchmarking
We benchmarked our model using a simple similarity test. The results of the test and method can be seen the [Model Performance Notebook](https://github.com/shiquan-lim/y3optim/blob/master/notebooks/Model%20Performance.ipynb)

## Instructions for starting Jupyter Notebook
1. Ensure that you have run through the steps in `Installation` to install the environment.
2. Activate the python environment with `source activate y3optim` (for Mac) or `activate y3optim` (for Windows).
3. Using terminal or command prompt, change the current directory to that of the notebook using `cd notebooks`
4. Start the Jupyter Notebook with `jupyter notebook`

