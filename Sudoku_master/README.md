# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: *First we set the local constaints to find naked_twins: 
1.length of box is 2, in local area; 
2.there is a pair-box have a the same value as target box in unit

After that we use these constraints to get all the naked_twins, we use them to modify box based on it*

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: *For Diagonal Suoku, I modify tthe eliminate and only_choice funtion. Local constaints are as follow:
1.box must in diagonal_1 = ['A1','B2','C3','D4','E5','F6','G7','H8','I9'] and diagonal_2 = ['I1','H2','G3','F4','E5','D6','C7','B8','A9']
2.box do not mondify itself

After we have these constraints, we propogate the result though all the boxes based on it. 
*

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
