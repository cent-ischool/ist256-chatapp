# IST256 Lesson 03
## Conditionals


- P4E Ch3


## Links

- Participation: [https://poll.ist256.com](https://poll.ist256.com)  (Sign in with *netid*@syr.edu and your SU Password.)
- Class Chat: [https://chat.ist256.com](https://chat.ist256.com)  (Microsoft Teams.)


# Agenda

- Homework 02 Solution
- Non-Linear Code Execution
- Relational and Logical Operators
- Different types of non-linear execution.
- Run-Time error handling


# Connect Activity 

A Boolean value is a/an ______?

 A. `True or False value`  
 B. `Zero-based value`  
 C. `Non-Negative value`  
 D. `Alphanumeric value`

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# What is a Boolean Expression?

- A **Boolean expression** evaluates to a **Boolean value** of <font color='red'> True </font> or <font color='green'> False </font>. 

- Boolean expressions ask questions.  
   - GPA >3.2  <span>&#8594;</span>  Is GPA greater than 3.2?  
   
- The result of which is <font color='red'> True </font> or <font color='green'> False </font> based on the evaluation of the expression:  
   - GPA = 4.0 <span>&#8594;</span>  GPA > 3.2  <span>&#8594;</span>  <font color='red'> True </font>  
   - GPA = 2.0 <span>&#8594;</span>  GPA > 3.2  <span>&#8594;</span>  <font color='green'> False </font>


# Program Flow Control with IF

- The **IF** statement is used to branch your code based on a Boolean expression.  
  


```python
if boolean-expression:
    statements-when-true
else:
    statemrnts-when-false
```

[![](https://mermaid.ink/img/pako:eNplULsOwjAM_JXIE0jND3RAghYmWICNMJjGpZXapEpcAar676QvCQlP9p0fd-4gs5oghryyr6xAx-J4VkaE2K5WYr2e8t3NMzLVZNjLV0FGsmvpPpHJH5lj5Rc27R7WVoRG0rtx5H1pTT9R-58LWyHlRqTzTCjENVwYMLH7AQ_D5hFNZmXj3H5WshQQQU2uxlIHa91AKuAiSFQQh1RTjm3FCpTpQyu2bC8fk0E8uIqgbXTwk5b4dFhDPLqJgHTJ1p2md41f67-9_WBU?type=png)](https://mermaid.live/edit#pako:eNplULsOwjAM_JXIE0jND3RAghYmWICNMJjGpZXapEpcAar676QvCQlP9p0fd-4gs5oghryyr6xAx-J4VkaE2K5WYr2e8t3NMzLVZNjLV0FGsmvpPpHJH5lj5Rc27R7WVoRG0rtx5H1pTT9R-58LWyHlRqTzTCjENVwYMLH7AQ_D5hFNZmXj3H5WshQQQU2uxlIHa91AKuAiSFQQh1RTjm3FCpTpQyu2bC8fk0E8uIqgbXTwk5b4dFhDPLqJgHTJ1p2md41f67-9_WBU)

# Python’s Relational Operators 

<table style="font-size:1.2em;">
    <thead><tr>
        <th>Operator</th>
        <th>What it does</th>
        <th>Examples</th>
    </tr></thead>
    <tbody>
    <tr>
        <td><code> > </code></td>
        <td> Greater than </td>
        <td> 4>2 (True)</td>
    </tr>
    <tr>
        <td><code> < </code></td>
        <td> Less than </td>
        <td> 4<2 (False)</td>
    </tr>
    <tr>
        <td><code> == </code></td>
        <td> Equal To </td>
        <td> 4==2 (False)</td>
    </tr>
    <tr>
        <td><code> != </code></td>
        <td> Not Equal To </td>
        <td> 4!=2 (True)</td>
    </tr>
    <tr>
        <td><code> >= </code></td>
        <td> Greater Than or Equal To </td>
        <td> 4>=2 (True)</td>
    <tr>
        <td><code> <= </code></td>
        <td> Less Than or Equal To </td>
        <td> 4<=2 (True)</td>
    </tr>
  </tbody>
</table>

Expressions consisting of relational operators evaluate to a **Boolean** value


# Watch Me Code 1!
```
  Do you need more milk?  
    
  When the Fudge family has less than 1 gallon of milk, 
  we need more!
```

# Check Yourself: Relational Operators

On Which line number is the Boolean expression True?  


```python
x = 15
y = 20
z = 2
x > y
z*x <= y
y >= x-z
z*10 == x
```

A. `4`  
B. `5`  
C. `6`  
D. `7`  
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Python’s Logical Operators

<table style="font-size:1.2em;">
    <thead><tr>
        <th>Operator</th>
        <th>What it does</th>
        <th>Examples</th>
    </tr></thead>
    <tbody>
    <tr>
        <td><code> and </code></td>
        <td> True only when both are True </td>
        <td> 4>2 and 4<5 (True)</td>
    </tr>
    <tr>
        <td><code> or </code></td>
        <td> False only when both are False </td>
        <td> 4<2 or 4==4 (True)</td>
    </tr>
    <tr>
        <td><code> not </code></td>
        <td> Negation(Opposite) </td>
        <td> not 4==2 (True)</td>
    </tr>
    <tr>
        <td><code> in </code></td>
        <td> Set operator </td>
        <td> 4 in [2,4,7] (True)</td>
    </tr>
  </tbody>
</table>



# Check Yourself: Logical Operators

On Which line number is the Boolean expression True?  


```python
raining = False
snowing = True
age = 45
age < 18 and raining
age >= 18 and not snowing
not snowing or not raining
age == 45 and not snowing
```

A. `4`  
B. `5`  
C. `6`  
D. `7`  
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Multiple Decisions: IF ladder

Use elif to make more than one decision in your if statement. Only one code block within the ladder is executed.


```python
if boolean-expression1:
    statements-when-exp1-true
elif boolean-expression2:
    statements-when-exp2-true
elif boolean-expression3:
    statements-when-exp3-true
else:
    statements-none-are-true
```

[![](https://mermaid.ink/img/pako:eNptkk9PxCAQxb8KmdNuUg6FnnowWWM96UW9WQ9YprZJCxtKs5qm3136hw3ocpr58TLwHkxQaYmQQ93pS9UIY8nTS6mIW6fDgRyPW32fTp9adygUxe-zoem8cxZz5jmPOd95kb4PVljsUdmBXhr086g1I37sInZbxCIRvy3ikSj7J1J604WqwOiJUHrn7HrbriWPohtwwc6ut_2Hc2874kUWjnlzJ640DYdcKQtHXCn3ua33KnxAUcejLvMdJNCj6UUr3fNOy24JtnFZlJC7UmItxs6WUKrZScVo9euPqiBfkklgPEsX3EMrvozoIa8XTwmgbK02z9uXWX_O_AsXZalz?type=png)](https://mermaid.live/edit#pako:eNptkk9PxCAQxb8KmdNuUg6FnnowWWM96UW9WQ9YprZJCxtKs5qm3136hw3ocpr58TLwHkxQaYmQQ93pS9UIY8nTS6mIW6fDgRyPW32fTp9adygUxe-zoem8cxZz5jmPOd95kb4PVljsUdmBXhr086g1I37sInZbxCIRvy3ikSj7J1J604WqwOiJUHrn7HrbriWPohtwwc6ut_2Hc2874kUWjnlzJ640DYdcKQtHXCn3ua33KnxAUcejLvMdJNCj6UUr3fNOy24JtnFZlJC7UmItxs6WUKrZScVo9euPqiBfkklgPEsX3EMrvozoIa8XTwmgbK02z9uXWX_O_AsXZalz)

# elif versus a series of if statements



```python
x = int(input("enter an integer"))
# one single statement. only one block executes
if x>10:
    print("A:bigger than 10")
elif x>20:
    print("A:bigger than 20")    
# Independent if's, each True Boolean executes a block
if x>10:
    print("B:bigger than 10")
if x>20:
    print("B:bigger than 20")
```

# Check Yourself: IF Statement

Assuming values ` x = 25 and y = 6` what value is printed?


```python
if x > 20:
    if y == 4:
        print("One")
    elif y > 4:
        print("Two")
    else:
        print("Three")
else:
    print("Four")
```

A. `One`  
B. `Two`  
C. `Three`  
D. `Four`  
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# End-To-End Example, Part 1:

### Tax Calculations!  
- The country of “Fudgebonia” determines your tax rate from the number of dependents:  
   - 0 <span>&#8594;</span> 30%  
   - 1 <span>&#8594;</span> 25%  
   - 2 <span>&#8594;</span> 18%   
   - 3 or more <span>&#8594;</span> 10%  
   
- Write a program to prompt for number of dependents (0-3) and annual income.  

- It should then calculate your tax rate and tax bill. Format numbers properly!  


# Handle Bad Input with Exceptions

- **Exceptions** represent a class of errors which occur at **run-time**. 
- We’ve seen these before when run a program and it crashes due to **bad input**. And we get a **TypeError** or **ValueError**.
- Python provides a mechanism **try .. except** to catch these errors at run-time and prevent your program from crashing.
- **Exceptions are <i>exceptional</i>**. They should ONLY be used to handle unforeseen errors in program input. 


# Try…Except…Finally

The Try... Except statement is used to handle exceptions. Remember that exceptions catch **run-time** errors!


```python
try:
    statements-which
    might-throw-an-error
except errorType1:
    code-when-Type1-happens
except errorType2:
    code-when-Type2-happens
finally:
    code-happens-regardless

```

# Watch Me Code 2

The need for an exception handling:
- Bad input
- try except finally
- Good practice of catching the specific error


## Check Yourself: Conditionals Try/Except

What prints on line 9 when you input the value **'-45s'**?


```python
try:
    x = float(input("Enter a number: "))
    if x > 0:
        y =  "a"
    else:
        y = "b"
except ValueError:
    y = "c"
print(y)
```

A. `'a'`  
B. `'b'`    
C. `'c'`
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)


# End-To-End Example, Part 2:

### Tax Calculations!
- Modify “Fudgebonia” tax calculations to handle bad inputs so that it will not generate run-time errors.


# Conclusion Activity Exit Ticket

### 1 Question Challenge  

When <font color='green'>x = 12, y = 20</font>   
What is the value of this Boolean expression?   
<font color='green'>x < y and not y==20</font>

A. True  
B. False  

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

