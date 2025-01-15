# Homework: Professor Charles Xavier's Teaching Assistant

## The Problem

Professor Charles Xavier has asked us to write a program to automatically calculate a final letter grade and grade points on a 4.0 scale forhis course based on an input point range. Here is the grading scale he uses: 

    Point Range Grade Grade Points
    125-150     A     4.0
    100-124     B     3.0
    75-99       C     2.0
    50-74       D     1.0
    0-49        F     0.0
    
  
Write a Python program to input a number of points earned and then outputs the letter grade and grade points.

For example, when 105 is the input:

    Professor Xavier's Grade Calculator
    Input the total points earned 0 to 150: 105
    Grade: B Grade Points: 3.0

Another example, when 50 is the input:

    Professor Xavier's Grade Calculator
    Input the total points earned 0 to 150: 50
    Grade: D Grade Points: 1.0


NOTE: You should store the grade and grade points in *variables*. **Do Not** `print()` each case explicitly! Input => Process => Output means we should not put input or output in our process!

GOOD: `print(f"Grade: {grade}...")`   
BAD:  `print("Grade: A...")`  

  
### Handling Bad Input

Your code should handle bad input. Specifically, there are two cases:

1. Your code should perform bounds checking of the input.  Valid inputs are in the range 0 to 150. Invalid inputs might be -1000 or 200, for exampl.e
2. Your code should handle non-integer input. Invalid inputs might 4.5 or "fifty".

For example, when 500 is the input:

    Professor Xavier's Grade Calculator
    Input the total points earned 0 to 150: 500
    Error: 500 is not in the range 0 to 150.

Another example, when huge is the input:

    Professor Xavier's Grade Calculator
    Input the total points earned 0 to 150: huge
    Error: input is not a number.

## Approach

We will use the **problem simplification** approach as learned in small group and the lab. First we solve a simpler problem, then we will solve the complete problem. There in this assignment you will write THREE programs!

- First in You Code 2.1 we will calculate the grade assuming the point range is a number between 0 and 150.
- Second in You Code 2.2 we re-write 2.1 to handle numbers outside the range 0 and 150
- Finally in You Code 2.3 we re-write 2.2 to handle bad inputs that are not numbers.


## Part 1: Problem Analysis

Once again we use the "working backwards approach"

### 1.1 Program Outputs

What is the program output. Describe it below.




### 1.2 Program Inputs

List out the program inputs in the cell below.




### 1.3 The Plan (Algorithm)

Explain, as specifically as you can, without writing code, how the program works from input to output. Be detailed with your plan as you will need to turn it into code. 




## Part 2: Code Solution

You may write your code in several cells, but place the complete, final working copy of your code solutions within the cell labeled `# SOLUTION CELL` everything required to make the code work should be in these cells, as per the instructions. 

### 2.1 You Code

In this first iteration. Solve the problem with the assumption that **the input values will always be a number between 0 and 150**. Do not worry about the other cases!



```python
# SOLUTION CELL 2.1

```

### 2.2 You Code

In this second iteration.  Solve the problem with the assumption that **the input values can be any number**.  You can start by copying your code from the previous solution cell, then adding the code so that it handles the other cases!


```python
# SOLUTION CELL 2.2

```

### 2.3 You Code

Finally re-write your code from 2.2 to handle inputs that are not numbers. You will need to use `try`... `except` to address the error.


```python
# SOLUTION CELL 2.3

```
