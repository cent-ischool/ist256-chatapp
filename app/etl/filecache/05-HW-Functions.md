# Homework: Paint Estimator 2.0

## The Problem


The big-box hardware store *House Depot* is back. They want you to improve upon the App you wrote previously that estimates the amount of paint required to paint a room.

Some of the program from the previous assignment will be the same but with the following two improvements:

**Improvement 1** House depot sells 3 different qualities of paint:

- 1 Gallon of **Everyday** paint costs 19.95 and covers 320 square feet  
- 1 Gallon of **Premium** paint costs 29.95 and covers 400 square feet  
- 1 Gallon of **Professional** paint costs 34.95 as covers 425 square feet  
    
**Improvement 2** You will write a user-friendly version of the program using IPywidgets and the `@interact_manual` decorator.
- **length** of the room is a slider from 1 to 40 feet
- **width** of the room is a slider from 1 to 40 feet
- **height** of walls is a slider from 6 to 10 feet in 0.5 ft increments
- **coats** is the number of coats of paint on the walls a sliders from 1 to 3
- **paint** is a drop-down of the 3 qualities of paint `['Everyday','Premium','Professional']`

Ultimately your program allows the user to input the dimensions of a room, number of coats, and select a paint quality. The program then outputs the square footage to be painted, gallons of paint (in whole gallons), and total cost of the paint.

## Approach

You will write this program in several phases.

- **You Code 2.1** write a function return the cost and coverage based on the type of paint input, `get_paint_info`
- **You Code 2.2** rewrite the House Depot assignment as a function, `calculate_paint_area`
- **You Code 2.3** write the final program to solve the problem, using your functions and regular `input` and `print` statements.
- **You Code 2.4** re-write the final program to use `@interact_manual` and the IPywidgets in place of `input` and `print` statements.

HINTS:

- Take a "bottom up" approach. Write each function first, test the function, then once you know it's right use the functions in your main program.
- The code exercise from small group demonstrates how to create drop-downs and sliders with ipython widgets
- If you use several code cells (which you probably will) make sure a copy  of all relevant code is in the code solution cell.
- The lab has functions you can re-use to print  out the big title. and display text. 

## Part 1: Problem Analysis

This time there should be multiple inputs / outputs / algos based on each function you will write.

### 1.1 Program Outputs

Describe your program outputs in the cell below. 


    outputs for get_paint_info function:

    outputs for calculate_paint_area function:
    
    outputs for main program:
    

### 1.2 Program Inputs

List out the program inputs in the cell below.


    inputs for get_paint_info function:

    inputs for calculate_paint_area function:

    inputs for main program:
    

### 1.3 The Plan (Algorithm)

Explain, as specifically as you can, without writing code, how the program works from input to output. Be detailed with your plan as you will need to turn it into code. 


    steps for get_paint_info function:

    steps for calculate_paint_area function:
       
    steps for main program:


## Part 2: Code Solution

You may write your code in several cells, but place the complete, final working copy of your code solution within  each cell labeled `# SOLUTION CELL` everything required to make the code work should be in this cell, as this is the cell that will get evaluated. 

### 2.1 You Code: write the `get_paint_info` function

Here you will implement **Improvement 1** and write the `get_paint_info` function. You are provided with a code skeleton to work from. DO NOT change the code skeleton, think about writing a program where the input is `paint_quality` (one of "Everyday", "Premium" or "Professional") and at the end you output `paint` and `coverage`, only the inputs are the arguments on the `def` line and the outputs are on the `return` line. This makes up the body of your function.

**ADVICE:** Consider this first part as two steps. Writing the `get_paint_info` function and testing it. For example if you look over the tests in the next cell, and what is *expected* that will  will help you understand how to write the function. You can try to get the first test to pass, then re-write the function to pass the next test, etc.


```python
# SOLUTION CELL 2.1
def get_paint_info(paint_quality):
    '''
    Given the paint_quality as input, this function returns
    the price per gallon, and coverage in square footage for the paint
    '''
    #TODO: write your code here in the function body

    return price, coverage
```

### Test cases for `get_paint_info`

Just like the only way to know for sure your program is correct is to run the code, the only way you know your function is correct is to call it! 

Below are 4 test cases written for you.  Make sure the function you write satisfies each test case. If **your code does not pass a test**, you will see miss-matched output to help you understand what you are doing wrong. Also an `AssertionError` will be thrown so that additional tests will not run.

NOTE: It might make sense to run this each time you change code in your function so that you are confident it still works. 



```python
def test_get_paint_info(quality, expected_price, expected_coverage):
    actual_price, actual_coverage = get_paint_info(quality)  # call the function and get actuals!
    print(f'get_paint_info("{quality}") should return ({expected_price}, {expected_coverage}) ACTUAL: ({actual_price}, {actual_coverage})')
    assert expected_price == actual_price and expected_coverage==actual_coverage 


test_get_paint_info(quality="Everyday", expected_price=19.95, expected_coverage=320) # TEST Everyday
test_get_paint_info(quality="Premium", expected_price=29.95, expected_coverage=400) # TEST Premium
test_get_paint_info(quality="Professional", expected_price=34.95, expected_coverage=425) # TEST Professional
test_get_paint_info(quality="Anything Else", expected_price=0, expected_coverage=0) # TEST Anything Else
```

### 2.2 You Code: write the `calculate_paint_area` function

Here you will rewrite the House Depot assignment as a function, `calculate_paint_area`. You are provided with a code skeleton below so you can just fill in the function body similar to 2.1



```python
# SOLUTION CELL 2.2
def calculate_paint_area(length, width, height, coats, paint_coverage):
    '''
        This function inputs :
        - the room dimension (length, width, height) in feet
        - the number of coats of paint on the room
        - the paint_coverage in sqft for the can of paint
        It outputs the `area_to_paint` of the room, `total_paint` based on number of coats 
        and `number_of_cans` required to complete the job.
    '''
    import math
    # TODO write your code here in the function body

    return area_to_paint, total_paint, number_of_cans
```

### Test cases for `calculate_paint_area`

The test cases for `calulate_paint_area` were chosen based on the `HW-Variables` Example runs. Again use these tests to have confidence your code is correct.


```python
def test_calculate_paint_area(length, width, height, coats, paint_coverage, expected_area, expected_total_paint, expected_cans):
    actual_area, actual_total_paint, actual_cans = calculate_paint_area(length, width, height, coats, paint_coverage)
    print(f'''calculate_paint_area(length, width, height, coats, paint_coverage) 
    should return ({expected_area}, {expected_total_paint}, {expected_cans})
    ACTUAL: ({actual_area}, {actual_total_paint}, {actual_cans})''')
    assert expected_area == actual_area \
        and expected_total_paint==actual_total_paint \
        and expected_cans == actual_cans

test_calculate_paint_area(length=12, width=14, height=8, coats=2, paint_coverage=400, 
                          expected_area=416, expected_total_paint=832, expected_cans=3) # HW-Variables.ipynb Example 1
test_calculate_paint_area(length=2, width=4, height=10, coats=3, paint_coverage=400, 
                          expected_area=120, expected_total_paint=360, expected_cans=1) # HW-Variables.ipynb Example 2
```

### 2.3 You Code- Entire Program

Write the final program to solve the problem, by calling your `get_paint_info` and `calculate_paint_area` functions. Use regular `input` and `print` statements. 

NOTES: 
 - Do not worry about handling bad inputs. You will get this for "Free" by using `@interact_manual` in 2.4
 - If you want the checker to work in this cell, 1) make sure your inputs are in the same order as the example run and 2) you need to copy your function definitions into this cell.


Example Run:

```
Enter length of room:  12
Enter width of room:  14
Enter height of room:  8
Enter number of coats:  2
Enter paint quality: Premium
Total area to be painted: 416.0 sqft
2.0 Coats requires: 832.0 sqft
1 Can of Premium paint covers 400 sqft
Total gallons of paint requried for 2.0 coats is : 3 cans of paint
```



```python
# SOLUTION CELL 2.3 

# Copy your function defintion for get_paint_info here

# Copy your function definition for calculate_paint_area here

# On with the MAIN PROGRAM
# INPUTS (nothing but input() statements here)

# PROCESS (nothing but youy 2 function calls here)

# OUTPUTS (nothing but print() statements here)

```

### 2.4 You Code - Ipywidgets

Complete the program by re-writing 2.3 using `@interact_manual`, which replaces your inputs with widgets.

**Improvement 2** You will write a user-friendly version of the program using IPywidgets and the `@interact_manual` decorator.
- **length** of the room is a slider from 1 to 40 feet
- **width** of the room is a slider from 1 to 40 feet
- **height** of walls is a slider from 6 to 10 feet in 0.5 ft increments
- **coats** is the number of coats of paint on the walls a sliders from 1 to 3
- **paint** is a drop-down of the 3 qualities of paint `['Everyday','Premium','Professional']`

Here's an example of the code running: https://imgur.com/a/MvKbw2u

NOTE: There is no automated code check for this cell. It will be graded manually.


```python
# SOLUTION CELL 2.4
from IPython.display import display, HTML
from ipywidgets import interact_manual

@interact_manual(WIDGETS)
def onclick(INPUTS):
    #TODO call functions and use display to output inside this function

```
