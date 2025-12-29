# IST256 Lesson 08
## Lists

- P4E Ch8

## Links

- Participation: [https://poll.ist256.com](https://poll.ist256.com)  
(Sign in with *netid*@syr.edu and your SU Password.)
- Class Chat: [https://chat.ist256.com](https://chat.ist256.com)  (Microsoft Teams.)



# FEQT (Future Exam Questions Training) 1

Which variable is the file handle?


```python
w = "mylist.txt"          # w file name 
x = "r"                 # x mode "r", "w", "a"
with open(w,x) as y:    # y - handle
    z = y.read()        # z = file contents

print(z)
```

 A. w  
 B. x  
 C. y   
 D. z  
 
## Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# FEQT (Future Exam Questions Training) 2

What is written to this file?


```python
w = "file.txt"
x = "w"
with open(w,x) as y:
    for i in range(3):
        y.write(f"{i}")
        
```

A. `0 1 2 3`   
B. `1 2 3`    
C. `0 1 2`    
D. None of the above  
 
## Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Agenda

### Homework 07

- Solution

### Lesson 08

- Lists as a mutable sequence of values.
- Indexing list values; slice notation.
- List functions and operations like add, remove, update, find
- Common patterns for list management.


# Connect Activity

For `x = [0,1,2,3,4,5]` what is  `x[2:4]` ?  
    
A. `[2,3]`  
B. `[1,2,3]`  
C. `[1,2]`  
D. `[2,3,4,5]`

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Lists are Mutable Sequence Types

- Python **lists** are variables which hold a collection of values. They are actually ***sequences of values***.
- Like strings, you can **index lists** and use **slice notation**.
- Unlike strings, lists are **mutable** which means *they can be changed*.
- In Python, type **list** is a ***sequence type***.


# Purpose of Lists

- Store collections of things. Stocks, grades, emails, words, etc...
- Easier to manipulate than a string or file (no need to tokenize/parse).
- Stored in the computer's memory, which is faster than files.

# Watch Me Code 1

###  List Enumeration and Aggregates
- Definite Loops
- Indexes / Slices
- List mutation
- Aggregations


# Check Yourself: List Indexes

- What is the value of the expression on line 2?
    



```python
grades = ['A', 'B+','A','C+','B-']
grades[:2]
```

A. `['A','B+','A']`  
B. `['A','B+']`  
C. `['B+','A']`  
D. `['A']`  
 
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# List Operations

Use the `+` operator to append combine two lists.

Note this does appends them - it does not remove duplicates or sort the list. 


```python
#List operators
x = [1,2,3]
y = [4,5,3]
z = x+y
z
```

# Built-In List Functions

- Like strings, Python lists have an assortment of built in functions for ***mutable sequence types***:

- For your reference:
https://docs.python.org/3/library/stdtypes.html?highlight=list#mutable-sequence-types

- Use your friends `dir()` and `help()`, too!


# Watch Me Code 2

### List Basics
- Empty Lists
- List Item Management
- Methods: append, remove, index


# Check Yourself 1: List Functions

## Match the Definition…! To its term.
Which list function **Adds anywhere in the list** ?


A. `insert`  
B. `remove`  
C. `append`  
D. `delete`

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Check Yourself 2: List Functions

## Match the Definition…! To its term.

Which list function **Deletes an item from the list** ?

A. `insert`  
B. `remove`  
C. `append`  
D. `delete`

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# End-To-End Example:

https://github.com/berzerk0/Probable-Wordlists

### Bad Password Checker
- Read in list of bad passwords from file
- Main program loop checks password  as "good" or "bad" password by checking if it exists in the file this repeats until user enters no password.
- Bad passwords are not on the list of passwords
- Got passwords from: https://raw.githubusercontent.com/berzerk0/Probable-Wordlists/master/Real-Passwords/Top12Thousand-probable-v2.txt
- Finally record history of attempted passwords to another list.

# Conclusion Activity: One Question Challenge

That is the value of `items` printed on line 6?



```python
items = ['a','b','c','d']
items.append('w')
items.remove('c')
items.insert(0,'x')
items.pop(1)
print(items)
```

A. `['a','b','c','d', 'w']`       
B. `['a','b','d', 'w']`  
C. `['x', 'b', 'd', 'w']`   
D. `['i','dont','know']`   

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)
