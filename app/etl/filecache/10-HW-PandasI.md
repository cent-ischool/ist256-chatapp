# Homework: iSchool Class Search

## The Problem

You have been hired to build an interactive data product for the iSchool that makes it easier for students to find classes. Your task is to read in a schedule of classes and create a user interface that allows someone to search the classes by:

    - Level: Gradudate / Undergraduate
    - Mode: Campus / Online
    - Meeting: MW / TuTh / MWF / etc...
    - Contents of the Course title
    
The program should then output a dataframe of the courses which match the selected criteria.

If this were a real-world project there would be two key steps 1) building the data pipeline to aquire the necessary data and then 2) building the user interface around the data. Because it an assignment this will be a simplified version.

The data can be found at the following URL: `https://raw.githubusercontent.com/mafudge/datasets/master/classes/ischool-schedule-fall2015.csv`

See the final product in action here: [https://imgur.com/a/MXTQZiX](https://imgur.com/a/MXTQZiX)


## Approach:

This assignment is broken up into parts. We will use problem simplification to solve this problem and take a bottom up approach, making the components, then assembling them together.

- **You Code 2.1** Load the data into a pandas dataframe
- **You Code 2.2** Data Cleanup
- **You Code 2.3** Engineer the Columns we Need
- **You Code 2.4** Building data for our widgets
- **You Code 2.5** Assemble the program from its parts

Since we are taking a bottom up approach, **hold off on completing part 1, until you are on step 2.5**


## Part 1: Problem Analysis

You will complete a problem analysis for the entire program. **Since we are using the bottom-up approach, do not attempt until step 2.5**


### 1.1 Program Outputs

Describe your program outputs in the cell below. 




### 1.2 Program Inputs

List out the program inputs in the cell below.




### 1.3 The Plan (Algorithm)

Explain, as specifically as you can, without writing code, how the program works from input to output. Be detailed with your plan as you will need to turn it into code. 




## Part 2: Code Solution

You may write your code in several cells, but place the complete, final working copy of your code solution within this single cell below. Only the within this cell will be considered your solution. Any imports or user-defined functions should be copied into this cell. 

### You Code 2.1: Load the data into a pandas datafrmae

In this first step, import the `pandas` and `numpy` libraries and then write code to load the dataset from the url found in the instructions at the top. Load into a Pandas DataFrame.

Also for your own sanity, you should probably ignore Pandas `filterwarnings`. We did this in the lab.

use the `print()` function to display the first 10 classes.  The code checker will scan this output so if you want this to pass you will need to use `print()` instead of `display()`

Just know that you can use `display()` while figuring it out, but if you want to pass the code checks, you'll habe to switch to `print()`


```python
# SOLUTION CELL 2.1

# FOR CHECKER: PRINT FIRST 10 ROWS

```

### You Code 2.2: Data Cleanup

If you look over the data with `info()` you will notice there are missing values in the `Instructor(s)`, `Day`, and `Room(s)` columns. We need to clean this data up before presenting it as the missing values showing `"NaN"` will be confusing to the users of our program.

Specifically do the following:

- in the `Instructor(s)` column replace all `NaN` with `"Staff"`. Its common for universities to use this label when the instructor is to be determined.
- in the `Room(s)` column replace `NaN` with `"TBA"`. Its common for universities to use this label when the room will be announced later TBA == To be Announced.
- in the `Day` column replace `NaN` with `"N/A"`. N/A means not applicable. 

TIPS : 

- use the column-selector then boolean filter approach used in the lab and small group: `df[col][boolean-index-selector] = value`
- your boolean index selector cannot compare the column to `np.nan` e.g. `col == np.nan` this is not the way to find nulls in a series!
- if you screw up your dataframe, don't fret just run 2.1 to reload it!

To pass the checker:
- include your solution to 2.1 WITHOUT the print
- add your code to replace the NaN columns
- print the first 2 rows in the dataframe, which should have these updated values.



```python
# SOLUTION CELL 2.2

# COPY CODE FROM 2.1 INCLUDE THE IMPORTS!


# YOUR CLEANUP CODE

# FOR CHECKER: PRINT FIRST TWO ROWS

```

### You Code 2.3 - Engineer the columns we need

Next we need to engineer two the columns. Here are the criteria:

- Column name `Level`, value is: 
  - `"Graduate"` number part of the course is >=500 , e.g. `IST625` (`625>=500`)
  - `"Undergraduate"` number part of the course is <500 e.g. `IST256 (`256<500`)  
  
-   
- Column name `Mode`, value is:
  - `"Online"` 2nd character in Section is an `"8"` e.g. `M800`
  - `"Campus"` 2nd character in Section is not an `"8"` e.g. `M012`
    
TIPS :

- Again, use the column-selector then boolean filter approach used in the lab and small group: `df[col][boolean-index-selector] = value`
- if you screw up your dataframe, don't fret just run 2.1 to reload it!

To pass the checker:

- include your solution to 2.1 WITHOUT the print
- add your code to replace the NaN columns
- print a slice of the dataframe from 98 to 104, which should have these updated values.



```python
# SOLUTION CELL 2.3

# COPY CODE FROM 2.1 INCLUDE THE IMPORTS!

# ENGINEER COLUMNS

# FOR CHECKER: PRINT SLICE FROM 100 to 106

```

### You Code 2.4 Buidling data for our widgets

Next we need to build the data for our dropdown input widgets. We need three:

1. a sorted list of unique non NaN values in the `Mode` Series, call this variable `modes`
2. a sorted list of unique non NaN values in the `Level` Series, call this variable `levels`
3. a sorted list of unique non NaN values in the `Day` Series, call this variable `days`

TIPS :

- Take the approach we used in the small group activity. 
- You do not need to create a custom widget here, just the Python lists of unique values.

To pass the checker:

- include your solutions from 2.1, 2.2 and 2.4 WITHOUT the print statements from those sections
- add your code create the three lists
- print the lists



```python
# SOLUTION CELL 2.4

# COPY CODE FROM 2.1, 2.2 and 2.3 

# CREATE LISTS

# FOR CHECKER: PRINT EACH LIST

```

### You Code 2.5 Assemble the final program as an interact

With all the components built, its time to consider the complete program.

- Complete the Problem Analysis Section above. 
  - What are the 4 inputs?
  - What is the 1 output?
  
TIPS: 

- As you write your algorithm remember you will peform steps 2.1 - 2.4 **before** you accept any input.
- the `on_click()` handler should filter the dataframe based on the inputs. This is similar to the Small Group exercise, but we will not need to create custom widgets the default ones are fine.
- Since there are 4 inputs, there should be 4 arguments to `@interact_manual` and the `on_click()` function.
- use `display()` to print the filtered dataframe.



```python
# SOLUTION CELL 2.5
import pandas as pd
import numpy as np
import warnings
from IPython.display import display, HTML
from ipywidgets import interact_manual
warnings.filterwarnings('ignore')


```
