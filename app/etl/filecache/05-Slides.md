# IST256 Lesson 05

## Functions

- P4E Ch 4

## Links

- Participation: [https://poll.ist256.com](https://poll.ist256.com)  (Sign in with *netid*@syr.edu and your SU Password.)
- Class Chat: [https://chat.ist256.com](https://chat.ist256.com)  (Microsoft Teams.)


# Agenda

- Exam Prep - Frequently Missed Question Types
- Homework 04 Review 

Functions:

- Using import for functions from a module.
- How to inspect module contents and get help on functions. 
- User-defined functions: arguments, named arguments, return values
- How to modularize our code with user-defined functions.


# Functions

- A **Function** is a named sequence of statements which accomplish a task. They promote modularity, making our code less complex, easier to understand and encourage code-reuse. 
- When you “run” a defined function it’s known as a **function call**. Functions are designed to be ***written once***, but ***called many times***.
- We've seen functions before:  


```python
# input(). random.randint(), and int() are all functions!
import random
x = input("Enter Name: ")  
y = random.randint(1,10)  #random is the module, randint() is the function
z = int("9")
```

# Functions, continued

- Functions are like their own little programs. They take input, which we call the **function arguments (or parameters)** and give us back output that we refer to as **return values**.

![Capture.PNG](Capture.PNG)



# Check Yourself 1: Functions

### Match the concept to its object name in the example.

   ### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <font color='green'> x = y(z) </font>
   
   #### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1. Function Name?
   &nbsp;&nbsp; A. `x`  
   &nbsp;&nbsp; B. `y`  
   &nbsp;&nbsp; C. `z`  
### Vote Now: [https://poll.cent-su.org](https://poll.cent-su.org)

# Check Yourself 2: Functions

### Match the concept to its object name in the example.

   ### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <font color='green'> x = y(z) </font>
   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Function Name?  
**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Argument?**  
   &nbsp;&nbsp; A. `x`  
   &nbsp;&nbsp; B. `y`  
   &nbsp;&nbsp; C. `z`  
### Vote Now: [https://poll.cent-su.org](https://poll.cent-su.org)

# Functions & Python Modules

- Python **modules** are separate files of Python functions.
- In an object-oriented context functions are called **Methods**. Methods are functions attached to a Python object variable.
- When you **import** a module, Python executes the and all the variables and methods/ functions module become available to your program. 
- In this example:
  - `random` is the Python object variable
  - `randint` is the Python method function for object variable `random`
  - `print()` is a Python function


```python
import random
x = random.randint(1,10)
print(x)
```

# dir() and help() built-in functions

- The **dir()** function will display the names defined by the module. This will help you find the method functions.
- You can get **help()** on any function name to see how to use it.
- In Jupyter the `?` at the end of the function will give you help.


```python
import random
dir(random)
help(random.randint)
random.randint?
```

# Watch Me Code 1

Import Modules:
- Import sys, math and random
- dir()
- help()
- `?`


# Built in Modules vs. External

- The Python language has several modules which are included with the base language: **Python Standard Library** https://docs.python.org/3/library/ 
- In addition you can import other libraries found on the Internet. 
- The Python Package Index is a website which allows you to search for other code avaialbe for use. https://pypi.org/
- Once you know which package you want, you can install it with the `pip` command from the terminal.
- example: `pip install <name-of-package>`

# Importing Modules 

Modules which are not built-in must be imported with the `import` command.


- `import foo` imports all code from module `foo`
- `from foo import bar,baz` only imports the `bar` and `baz` functions from module `foo`
- `import foo as f` imports all code from module `foo` and renames it to `f` (usually to avoid naming conflicts)

# Installing Modules you Don't have 

- Find code modules at the Python Package Index [https://pypi.org](https://pypi.org)
- Other people's code published as a package you can download and install.
- Use the package installer, `pip` to install in your own Python environment.
- In notebook cell `!pip install <modulename>` 


# Watch Me Code 2: 

### Let's Do Text to Speech in Python!

- use Pypi https://pypi.org/ to find a Python package... gTTS
- import the Python package into our environment using `pip` 
- demonstrate different ways you can use `import` to bring in the code we need.
- use `dir()` and `help()` to figure things out.


# Check Yourself 3: modules


To figure out which functions are in a module we use ?

A. `pip`  
B. `import`  
C. `dir`  
D. `help`


### Vote Now: [https://poll.cent-su.org](https://poll.cent-su.org)

# Check Yourself 4: modules

To load an installed module into the Python environment so you can use it, we use ?

A. `pip`  
B. `import`  
C. `dir`  
D. `help`


### Vote Now: [https://poll.cent-su.org](https://poll.cent-su.org)

# Check Yourself 5: modules

To download and install a package of modules into the Python environment, we use ?

A. `pip`  
B. `import`  
C. `dir`  
D. `help`


### Vote Now: [https://poll.cent-su.org](https://poll.cent-su.org)

# User-Defined Functions

- We can create out own functions with Python's  **def** statement. 
- Function are like little programs with inputs and outputs. 
- function inputs go in the `()` after the function name. These are called the **arguments** of the function.
- Functions outputs are specified in a `return` statement within your function code. 


```python
# arguments are input into the function
# return is the output
def my_function_name(input_arguments):
      statements-in-function
      return output_expression
```

# Watch Me Code 3

### User defined text to speech function

- Functions make code readable and promote re-use!
- Concept: Named Arguments for language or accent


# Function Variable Scope

- Variables defined outside any function are **Global Variables**. These  are accessible ***from everywhere*** including inside function definitions.
- Variables defined inside a function are **Local Variables**, and are only accessible inside the function definition.
- Local variables with the same name take precedence over global variables 
- **Best Practice: <font color='green'> Avoid Global Variable Use In Functions!!! </font>**


# Scope Example

- `a` = local to function `x()`
- `b` = global scope
- `c` = value of "d" in function `x()` value of "t" globally


```python
b = "a"
c = "t"
def x(a):
    c = "d"
    return a+b+c 
print(x("p"))
print(c) 
```

# IPython display and interact 

- Now that we covered functions we can write programs with better input/output!
- `IPython.display` for output
- `ipywdgets.interact` and `interact_manual` for better input.
- Write a function to do something
- decorate with `interact_manual()`

# Watch Me Code 4

### IPython Interactive

- Write a function call the `speak()` function we wrote.
- call with `@interact_manual` so arguments can be entered at run time.


# End-To-End Example:

Fred's Fence Calculator Interact Edition
- re-Write fred's fence as a function
- test it.
- write an interact function.



# Conclusion Activity Exit Ticket

### One Question Challenge

What is the value printed on the last line?



```python
def myfunc(y):
    x = 1
    z = x + y + a
    return z

a = 2
b = myfunc(2)
print(b)
```

A. `NameError`  
B. `3`  
C. `5`  
D. `4`


### Vote Now: [https://poll.cent-su.org](https://poll.cent-su.org)
