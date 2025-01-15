# Class Coding Lab: Introduction to Programming

The goals of this lab are to help you to understand:

1. How to turn in your lab and homework
2. the Jupyter programming environments
3. basic Python Syntax
4. variables and their use
5. how to sequence instructions together into a cohesive program
6. the input() function for input and print() function for output


## Let's start with an example: Hello, world!

This program asks for your name as input, then says hello to you as output. Most often it's the first program you write when learning a new programming language. 

TO RUN THIS CODE: Click in the cell below and click the run cell button.

NOTE: After the code executes, you will see a sequence number next to the code and output below the code itself. This is your indication the code in the cell has run. You must run all code cells in the notebook for full credit.



```python
your_name = input("What is your name? ")
print('Hello there',your_name)
```

Believe it or not there's a lot going on in this simple two-line program, so let's break it down.

 - **The first line:**
  - Asks you for input, prompting you with `What is your Name?`
  - It then stores your input in the variable `your_name` 
 - **The second line:**
  - prints out the following text: `Hello there`
  - then prints out the contents of the variable `your_name`

At this point you might have a few questions. What is a variable? Why do I need it? Why is this two lines? Etc... All will be revealed in time.

## Variables

Variables are names in our code which store values. I think of variables as cardboard boxes. Boxes hold things. Variables hold things. The name of the variable is on the ouside of the box (that way you know which box it is), and value of the variable represents the contents of the box. 

### Variable Assignment

**Assignment** is an operation where we store data in our variable. It's like packing something up in the box.

In this example we assign the value "USA" to the variable **country**


```python
# Here's an example of variable assignment. 
country = 'USA'
```

### Variable Access  

What good is storing data if you cannot retrieve it? Lucky for us, retrieving the data in variable is as simple as calling its name:


```python
country # Run this cell. It should say 'USA'
```

At this point you might be thinking: Can I overwrite a variable? The answer, of course, is yes! Just re-assign it a different value:


```python
country = 'Canada'
```

You can also access a variable multiple times. Each time it simply gives you its value:


```python
country, country, country
```

### The Purpose Of Variables

Variables play an vital role in programming. Computer instructions have no memory of each other. That is one line of code has no idea what is happening in the other lines of code. The only way we can "connect" what happens from one line to the next is through variables. 

For example, if we re-write the Hello, World program at the top of the page without variables, we get the following:



```python
input("What is your name? ")
print('Hello there')
```

When you execute this program, notice there is no longer a connection between the input and the output. In fact, the input on line 1 doesn't matter because the output on line 2 doesn't know about it. It cannot because we never stored the results of the input into a variable!

### 1.1 You Code

Re-write the program above to input a name and then say hello there, name. It will need to store the first line in a variable so that it can be printed on the 2nd line.


```python
# TODO: Write your code here

```

### What's in a name? Um, EVERYTHING

Computer code serves two equally important purposes:

1. To solve a problem (obviously)
2. To communicate how you solved problem to another person (hmmm... I didn't think of that!)

If our code does something useful, like land a rocket, predict the weather, or calculate month-end account balances then the chances are 100% certain that *someone else will need to read and understand our code.*  

Therefore it's just as important we develop code that is easily understood by both the computer and our colleagues.

This starts with the names we choose for our variables. Consider the following program:


```python
y = input("Enter your city: ")
x = input("Enter your state: ")
print(x,y,'is a nice place to live')
```

What do `x` and `y` represent? Is there a semantic (design) error in this program?

You might find it easy to figure out the answers to these questions, but consider this more human-friendly version:


```python
city = input("Enter your city: ")
state = input("Enter your state: ")
print(city, state, 'is a nice place to live')
```

Do the aptly-named variables make it easier to find the semantic errors in this second version? OF COURSE THEY DO!!!

### 1.2 You Code

**Debug** the program below (remove errors to get it working). When it is correct it should input your name and your age and the print name and age on a single line. Make sure you use aptly-named variables!!!

Example of the Program running:
```
Enter your name: Mike
Enter your age: 25
Mike is 25
```
In the above example `Mike` was the entered name, and `25` was the entered age. 


```python
# TODO: Debug this code here.
name = input "Enter your name: "
foo = input("Enter your age: ")
print(name, "is" )

```

### 1.3 You Code

Now try to write a program which asks for two separate inputs: your first name and your last name. The program should then output `Hello` with your first name and last name.

For example if you enter `Mike` for the first name and `Fudge` for the last name the program should output `Hello Mike Fudge`

**HINTS**

 - Use appropriate variable names. If you need to create a two word variable name use an underscore in place of the space between the words. eg. `two_words` 
 - You will need a separate set of inputs for each name.



```python
# TODO: write your code here

```

### Variable Concatenation: Your First Operator

The `+` symbol is used to combine to variables containing text values together. Consider the following example:


```python
prefix = "re"
suffix = "ment"
root = input("Enter a root word, like 'ship': ")
print( prefix + root + suffix)
```


```python
first = input("Enter first name: ")
last = input("enter last name: ")
name_last_first = last + "," + first
print(name_last_first)
```

### 1.4 You Code

Write a program to prompt for three colors as input, then outputs those three colors in order they were entered, informing me which one was the middle (2nd entered) color. 

For example if you were to input  `red` then `green` then `blue`   

the program would output:   
`Your colors are: red, green, and blue.`  
`The middle color is green.` 

**HINTS**

 - you'll need three variables one for each input
 - you should try to make the program output like my example. This includes commas and the word `and`. 
 - name your variables appropriately!
 - use the `+` operator.
 


```python
# TODO: write your code here

```

### F-Strings

In Python 3.7, f-strings were introduced to make it easier to format string literals in the `print()` statement. 

Here's how it works:

- Put an `f` in front of the string literal, like this: `f"`
- For any variable you want to print, enclose in `{curly braces}` within the string literal.
- At run-time the variable in `{curly braces}` is replaced with its value! This is called **string interpolation**.

For example:


```python
name = "Mary"
major = "Data Science"
gpa = "4.0"
print(f"{name} is a {major} major. Her gpa is {gpa}")
```

### 1.5 You Code

Re-write the last program (1.4 You Code) to print using f-strings! As good practice, do not copy and paste code, instead re-write it. This will result in fewer bugs (mistakes) in your code.


```python
# TODO: write your code here

```

##  Metacognition


### Rate your comfort level with this week's material so far.   

**1** ==> I don't understand this at all yet and need extra help. If you choose this please try to articulate that which you do not understand to the best of your ability in the questions and comments section below.  
**2** ==> I can do this with help or guidance from other people or resources. If you choose this level, please indicate HOW this person helped you in the questions and comments section below.   
**3** ==> I can do this on my own without any help.   
**4** ==> I can do this on my own and can explain/teach how to do it to others.

`ENTER A NUMBER 1-4 IN THE CELL BELOW`

3

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
