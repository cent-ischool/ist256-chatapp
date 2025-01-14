# Homework: Grade Distributions

## The Problem

Professor Charles Xavier is at it again. He would like you to improve on the program you wrote for him last week. As you may recall this program, when given an input of a student points earned in the course, would output a letter grade and grade points.

Prof. Xavier would like the program to input multiple points earned as part of a sentinel controlled loop, and as each student total point score is entered calculate the following statistics:

- count of student point scores in "A" range, and percentage of total
- count of student point scores in "B" range, and percentage of total
- count of student point scores in "C" range, and percentage of total
- count of student point scores in "D" range, and percentage of total
- count of student point scores in "F" range, and percentage of total
- total count of point scores entered

NOTE: The statistics are only displayed when the command `quit` is entered.

Once again, here is the grading scale he uses: 

    Point Range Grade Grade Points
    125-150     A     4.0
    100-124     B     3.0
    75-99       C     2.0
    50-74       D     1.0
    0-49        F     0.0
    
Sample Run 1:

    Enter student score or 'quit' to exit: 130
    Enter student score or 'quit' to exit: 111
    Enter student score or 'quit' to exit: 145
    Enter student score or 'quit' to exit: quit
        Scores : 3
        A: 2 (66%)
        B: 1 (33%)
        C: 0 (0%)
        D: 0 (0%)
        F: 0 (0%)
   
Sample Run 2:

    Enter student score or 'quit' to exit: 130
    Enter student score or 'quit' to exit: 111
    Enter student score or 'quit' to exit: 145
    Enter student score or 'quit' to exit: 100
    Enter student score or 'quit' to exit: 60
    Enter student score or 'quit' to exit: quit
        Scores: 5
        A: 2 (40%)
        B: 2 (40%)
        C: 0 (0%)
        D: 1 (20%)
        F: 0 (0%)

    
HINTS: **use problem simplification** like we did in small group and the lab!

- First in You Code 2.1: Write a loop to input grades. Just count the number of grades inputted (Scores). Accept string input, checking for 'quit', when its not 'quit', convert to a `int` and then count it. Upon quit, display the count of scores entered.
- Second in You Code 2.2: Inside your loop, figure out what grade the score is based in the input. You will use a series of `if` statements similar to the previous homework assignment. For example, if the score is an "A" increment a variable that counts the number of "A" grades. Upon quit display the score and grades. 


## Part 1: Problem Analysis

Once again we use the "working backwards approach"

### 1.1 Program Outputs

Describe the program outputs below.




### 1.2 Program Inputs

List out the program inputs in the cell below. 




### 1.3 The Plan (Algorithm)

Explain, as specifically as you can, without writing code, how the program works from input to output. Be detailed with your plan as you will need to turn it into code. 




## Part 2: Code Solution

You may write your code in several cells, but place the complete, final working copy of your code solution within the cell labeled `# SOLUTION CELL` everything required to make the code work should be in this cell, as this is the cell that will get evaluated. 

### 2.1 You Code

Write a loop to input grades. Just count the number of grades inputted (Scores). Accept string input, checking for 'quit', when its not 'quit', convert to a `int` and then count it. Upon quit, display the count of scores entered. `Scores: ?`


```python
# SOLUTION CELL 2.1

```

### 2.2 You Code

Inside your loop, figure out what grade the score is based in the input. You will use a series of `if` statements similar to the previous homework assignment. For example, if the score is an "A" increment a variable that counts the number of "A" grades. Upon quit display the score and grades. 

Start with a copy of your answer from 2.1


```python
# SOLUTION CELL 2.2

```

### 2.3 Optional Bar Chart Challenge!

This is optional and will not be graded, or factored into the assignment checker.

#### If you want in the X-men you need to suck up to Prof. Xavier!!!

Print your stats using a text-only tech bar chart, like this. This is easy to do in Python with the `*` string operator. Look it up and make it your own!

    Scores : 30
    A | ************ 12 (40%)
    B | ********* 9 (30%)
    C | *** 3 (10%)
    D | ****** 6 (20%)
    F | (0%)


```python
# SOLUTION CELL 2.3 (optional)

```
