# Class Coding Lab: Variables And Types

The goals of this lab are to help you to understand:

1. Python data types
1. Getting input as different types
1. Formatting output as different types
1. Basic arithmetic operators
1. How to create a program from an idea.

## Variable Types

Every Python variable has a **type**. The Type determines how the data is stored in the computer's memory: 


```python
a = "4"
type(a) # should be str
```


```python
a = 4
type(a) # should be int
```

### Types Matter 

Python's built in functions and operators work differently depending on the type of the variable.:


```python
a = 4
b = 5
a + b # the "+" in this case means add so 9
```


```python
a = "4"
b = "5"
a + b # the "+" in this case means concatenation, so '45'
```

### Switching Types

there are built-in Python functions for switching types. For example:


```python
x = "45" # x is a str
y = int(x)  # y is now an int
z = float(x) # z is a float
print(x,y,z)
```

### Inputs type str

When you use the `input()` function the result is of type `str`:



```python
age = input("Enter your age: ")
type(age)
```

We can use a built in Python function to convert the type from `str` to our desired type:


```python
age = input("Enter your age: ")
age = int(age)
type(age)
```

We typically combine the first two lines into one expression like this:


```python
age = int(input("Enter your age: "))
type(age)
```

### 1.1 You Code: Debuging

The following program has errors in it. Your task is to fix the errors so that:

- your age can be input and convertred to an integer.
- the program outputs your age and your age next year. 

For example:
```
Enter your age: 45
Today you are 45 next year you will be 46
```


```python
# TODO: Debug this code
age = int(input("Enter your age: "))
nextage = age + 1
print(f"Today you are {age} next year you will be {nextage}")
```

## Format Codes

Python has some string format codes which allow us to control the output of our variables. 

- %s = format variable as str
- %d = format variable as int
- %f = format variable as float

You can also include the number of spaces to use for example `%5.2f` prints a float with 5 spaces 2 to the right of the decimal point.


```python
name = "Mike"
age = 45
gpa = 3.4
print("%s is %d years old. His gpa is %.3f" % (name, age,gpa))
# Type inference
```

## Formatting with F-Strings

The other method of formatting data in Python is F-strings. As we saw in the last lab, F-strings use interpolation to specify the variables we would like to print in-line with the print string.

You can format an f-string

- `{var:d}` formats `var` as integer
- `{var:f}` formats `var` as float
- `{var:.3f}` formats `var` as float to `3` decimal places.

Example:


```python
name ="Mike"
wage = 15
print(f"{name} makes ${wage:.2f} per hour")
```

### 1.2 You Code

Re-write the program from (1.1 You Code) so that the print statement uses format codes. Remember: do not copy code, as practice, re-write it.



```python
# TODO: Write code here

```

### 1.3 You Code

Use F-strings or format codes to Print the PI variable out 3 times. 

- Once as a string, 
- Once as an int, and 
- Once as a float to 4 decimal places. 



```python
#TODO: Write Code Here
```

## Putting it all together: Fred's Fence Estimator

Fred's Fence has hired you to write a program to  estimate the cost of their fencing projects. For a given length and width you will calculate the number of 6 foot fence sections, and the total cost of the project. Each fence section costs $23.95. Assume the posts and labor are free.

Program Inputs:

- Length of yard in feet
- Width of yard in feet
    
Program Outputs:

- Perimeter of yard ( 2 x (Length + Width))
- Number of fence sections required (Permiemer divided by 6 )
- Total cost for fence ( fence sections multiplied by $23.95 )
    
NOTE: All outputs should be formatted to 2 decimal places: e.g. 123.05 

```
#TODO:
# 1. Input length of yard as float, assign to a variable
# 2. Input Width of yard as float, assign to a variable
# 3. Calculate perimeter of yard, assign to a variable
# 4. calculate number of fence sections, assign to a variable 
# 5. calculate total cost, assign to variable
# 6. print perimeter of yard
# 7. print number of fence sections
# 8. print total cost for fence. 
```

### 1.4 You Code

Based on the provided TODO, write the program in python in the cell below. Your solution should have 8 lines of code, one for each TODO.

**HINT**: Don't try to write the program in one sitting. Instead write a line of code, run it, verify it works and fix any issues with it before writing the next line of code. 


```python
# TODO: Write your code here

```

## Metacognition



### Rate your comfort level with this week's material so far.   

**1** ==> I don't understand this at all yet and need extra help. If you choose this please try to articulate that which you do not understand to the best of your ability in the questions and comments section below.  
**2** ==> I can do this with help or guidance from other people or resources. If you choose this level, please indicate HOW this person helped you in the questions and comments section below.   
**3** ==> I can do this on my own without any help.   
**4** ==> I can do this on my own and can explain/teach how to do it to others.

`ENTER A NUMBER 1-4 IN THE CELL BELOW`



###  Questions And Comments 

Record any questions or comments you have about this lab that you would like to discuss in your recitation. It is expected you will have questions if you  complete this assignment.  Learning how to articulate what you do not understand is an important skill of critical thinking. Write your questions below so that you remember to ask them in your recitation. We expect you will take responsilbity for your learning and ask questions in class.

`ENTER YOUR QUESTIONS/COMMENTS IN THE CELL BELOW`  





## How Do I hand in my Work?

FIRST AND FOREMOST: **Save Your work!** Yes, it auto-saves, but you should get in the habit of saving before submitting. From the menu, choose File --> Save Notebook. Or you can use the shortcut keys `CTRL+S`

### Lab Check

Check your lab before submitting. Look for errors and incomplete parts which might cost you a better grade


```python
from casstools.notebook_tools import NotebookFile
NotebookFile().check_lab()
```

### Lab Submission

Run this code and follow the instructions to turn in your lab. 


```python
from casstools.assignment import Assignment
Assignment().submit()
```
