# Introduction
This is an application created for [Y3 Technologies](http://www.y3technologies.com) built by [Lim Shi Quan](https://github.com/shiquan-lim), [Russell Yap](https://github.com/russellyap), [Gideon Raj]() and [Amos Tan](https://github.com/atwj) as a project for an Singapore Management University, School Of Information Systems elective: __IS421 – Enterprise Analytics for Decision Support__.

The purpose of this project is to design and built an application that takes in information about a customer (such as age and budget), will recommend a set of items that will maximize the customer's satisfaction.

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
- ```main.py``` is a command line application. To use the application, we assume that the user has set up the database and run the ```data.py``` script that will load the tables required by the application. </br>

## data.py
