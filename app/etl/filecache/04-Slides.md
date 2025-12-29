# IST256 Lesson 04
## Iterations

- P4E Ch5

## Links

- Participation: [https://poll.ist256.com](https://poll.ist256.com)  (Sign in with *netid*@syr.edu and your SU Password.)
- Class Chat: [https://chat.ist256.com](https://chat.ist256.com)  (Microsoft Teams.)


# Agenda

- Exam 1
- Go over HW 03

### Iterations 
- Make our code execute in a non linear fashion.
- Definite loops (for loops) and iterators.
- Indefinite looping, infinite loops, and the break and continue statements
- How to build complex loops easily. 


# Connect Activity

Select the line number where the **increment** occurs: 


```python
i,j,k = 1, 20, 1
while (i<j):
    n = k*(j-i)
    print(n)
    i = i + 1
    j = j - 1
    k = k * 5
```

A. `4`  
B. `5`  
C. `6`  
D. `7`  

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Increment and Decrement

- **Increment** means to add a value to a variable.  
  `X = X + 1`
- **Decrement** means to subtract a value from a variable.  
  `X = X - 1`
- These are common patterns in iteration statements which you will see today. 


# Anatomy of a loop

- A **Loop** is a sequence of code that repeats as long as a Boolean expression is <font color="green">True </font>. 



```python
x = 1
while x <= 7:
    x = x + 1

```

    False


- The sequence of code that repeats is known as the **Body**.
- The Boolean expression which is tested is known as the **Test Condition** or **Exit Condition**.
- Variables which are part of the Test condition are called **Loop Control Variables** or **Iteration Variables**. 
- Our goal is to make the Test condition False so that the loop stops. This is accomplished through changing the loop control variable within the body of the loop.

# Watch Me Code 1

  ## Say My Name:
- This program will say you name a number of times.
- This is an example of a **Definite loop** because the number of iterations are pre-determined.


# Check Yourself: Loop

on which line is the test / exit condition?


```python
x = 1
while x<5:
    print(x, end=" ")
    x = x + 1
    
print(x)
```

A. `1`  
B. `2`  
C. `3`  
D. `4`  

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# For Loop

- The **For Loop** iterates over a python list, string, or range of numbers. 
- It is the preferred statement for **Definite loops**, where the number of iterations are pre-determined. Definite loops do not require an exit condition.
- The for loop uses an **iterator** to select each item from the list or range and take action in the loop body. 
- The **range()** function is useful for getting an iterator of numbers.
- The for loop and iterate over any iterable. 



```python
for i in range(3):
    print("Hello ")
    
for char in "mike":
    print (char)
```

# Range

- The `range()` function returns an iterable.
- `range(n)` returns `n` iterations from `0` to `n-1`


```python
print("range(10) =>", list(range(10)) )
print("range(1,10) =>", list(range(1,10)) )
print("range(1,10,2) =>",list(range(1,10,2)) )
```

# Watch Me Code 2

## Say My Name:

- Range() function
- ***Refactored*** as a For Loop.


# Check Yourself: For Range 1

How many iterations are in this loop? 


```python
k = 0
j = 10
for j in range(5):
    k = k + j
    print(k)
```

A. `0`  
B. `10`  
C. `5`  
D. `Unknown`  

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Check Yourself: For Range 2

What is the value of k on line 4?



```python
k = 0
for j in range(5): 
    print(f"k={k},j={j},k+j={k+j}")
    k = k + j	
print(k)
```

A. `0`  
B. `10`  
C. `5`  
D. `15`  

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Watch Me Code 3

## Count the "i"'s 
- Definite Loop


# Indefinite,Infinite Loops and Break

- The **Indefinite Loop** has no pre-determined exit condition. There are no guarantees an indefinite loop will end, as it is typically based on user input.
- **Infinite Loops** are loops which can never reach their exit condition. These should be avoided at all costs.
- The **break** statement is used to exit a loop immediately.It is often used to force an exit condition in the body of the loop.


# Indefinite Loops The Easy Way

1. Determine the code to repeat
2. Determine the loop control variables & exit conditions
3. Write exit conditions as **if** statements with **break**
4. Wrap the code in a **while True:** loop!


# Watch Me Code 4

## Guess My Name:
- This program will execute until you guess my name. 
- Uses the indefinite loop approach.

# Check Yourself: Loop Matching 1

A loop where the test condition is never false is known as which kind of loop?
   
 A. `Break`  
 B. `Infinite`  
 C. `Definite`  
 D. `Indefinite`  
   
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)
   

# Check Yourself: Loop Matching 2

The Python keyword to exit a loop is?
   
 A. `break`  
 B. `exit`  
 C. `quit`  
 D. `while`  
   
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)
   
   

# End-To-End Example

## Password Program:
- 5 attempts for the password
- On correct password, print: “Access Granted”, then end the program 
- On incorrect password “Invalid Password Attempt #” and give the user another try
- After 5 attempts, print “You are locked out”. Then end the program.


# Conclusion Activity Exit Ticket

This program will output?



```python
for x in 'mike':
    if x == 'k':
        print('x', end="")
    else:
        print('o', end="")
```

A. `xo`  
B. `ox`  
C. `ooxo`  
D. `xxox`  

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)
