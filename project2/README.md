Project 2
by
Arnar Bragi Bragason   -   arnarbb21@ru.is
Haraldur Jón Friðriksson - haraldurf21@ru.is

We wanted to include this read me so you could get a quick overview of what to find in our files.

agent.py:
    Contains the a search class consisting of functions that contribute to solving the boards.
    Different combinations of algorithms and heuristics along with helper functions.

environment.py:
    Sort of like a wrapper for search and board generation. Initalizes a board with the right parameters and then you can call a function to solve it.

generator.py:
    Most of the code in this file is borrowed from: https://www.geeksforgeeks.org/program-sudoku-generator/
    We use it to generate boards of different sizes and difficulty.

main.py:
    Here we created an interface so that a user can choose different settings for a puzzle and then choose how it should be so solved (algorithm x heuristic).

mrv_queue.py:
    Contains a class used to keep track of the empty squares and keep them in MRV order.

state.py:
    Used to print boards and carry out the creation of boards from the environment.

tests.py:
    In this file you will find the function that created our test files and the function that ran the tests.

    If you wish to run a set of tests you have to make a call to the 'test' function with the size of the board, name of the algorithm and the right list of file names.

    For example: test(9, "backtracking_brute", TESTS_9x9)
    Where 9 is the size, "backtracking_brute" is the algorithm and TESTS_9x9 is a list containing the local test files, TESTS_9x9 = ["9x9_EASY.txt", "9x9_MEDIUM.txt", "9x9_HARD.txt"].
