# IST256 Lesson 02
## Input, Output, Variables and Types


- Severance Ch 2

## Links

- Participation: [https://poll.ist256.com](https://poll.ist256.com)  (Sign in with *netid*@syr.edu and your SU Password.)
- Class Chat: [https://chat.ist256.com](https://chat.ist256.com)  (Microsoft Teams.)


# Agenda

- What is a variable? What is its purpose?
- Different data types for variables.
- Type checks and conversions.
- Print variables of different types with formatting
- Input variables of different types. 
- Arithmetic expressions, arithmetic operators, and operands.

# Just A Note About Large Group

- I will write code in class. 
- Do NOT try to code along with me. It will only frustrate you. 
- Instead observe, take notes ask questions and participate!
- I will give you the code later. In some cases you have the code already.
- Large group should be interactive!


# Connect Activity 

These statements are out of sequence, which letter represents the 3rd step in this program?:

A. `print("Hello", name)`  
B. `fn=input("Enter First Name:")`  
C. `name = fn + " " + ln`    
D. `ln=input("Enter Last Name:")`   

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)



# Variables

- **Variables** are named areas of computer memory for storing data. 
- The **name** can be anything but should make symbolic sense to the programmer.
- We **write** to the variable’s memory location with the assignment statement (=)
- We **read** from the variable by calling its name. 
- Variable names must begin with a letter or _ and must only contain letters, numbers or _.


# Variables, Types and Assignment


![](https://i.imgur.com/TtTNDFx.png)


# Variables are of a Specific Type

<table style="font-size:1.2em;">
    <thead><tr>
        <th>Type</th>
        <th>Purpose</th>
        <th>Examples</th>
    </tr></thead>
    <tbody>
    <tr>
        <td><code>int</code></td>
        <td>Numeric type for integers only</td>
        <td>45, -10</td>
    </tr>
    <tr>
        <td><code>float</code></td>
        <td>Numeric type floating point numbers</td>
        <td>45, -10</td>
    </tr>
    <tr>
        <td><code>bool</code></td>
        <td>True or False values</td>
        <td>True, False</td>
    </tr>
    <tr>
        <td><code>str</code></td>
        <td>Characters and text</td>
        <td>"A", 'Mike'</td>
    </tr>
  </tbody>
</table>

# Type Detection and Conversion 

<table style="font-size:1.2em;">
    <thead><tr>
        <th>Python Function</th>
        <th>What It Does</th>
        <th>Example of Use</th>
    </tr></thead>
    <tbody>
    <tr>
        <td><code>type(<em>n</em>)</code></td>
        <td>Returns the current type of <em>n</em></td>
        <td><code>type(13) == int</code></td>
    </tr>
    <tr>
        <td><code>int(<em>n</em>)</code></td>
        <td>Converts <em>n</em> to type <b>int</b></td>
        <td><code>int("45") == 45</code></td>
    </tr>
    <tr>
        <td><code>float(<em>n</em>)</code></td>
        <td>Converts <em>n</em> to type <b>float</b></td>
        <td><code>float(45) == 45.0</code></td>
    </tr>
    <tr>
        <td><code>str(<em>n</em>)</code></td>
        <td>Converts <em>n</em> to type <b>str</b></td>
        <td><code>str(4.0) == '4.0'</code></td>
    </tr>
  </tbody>
</table>

# Watch Me Code 1

### Understanding Variables and Types !

- Assignment
- Variables of Different Types
- Switching Types, Type Conversion
- Checking types with `type()`
- Combining `input()` with `int()`, or `float()`

# Check Yourself: Which Type 1?

What is the value of `str(314)` ?

A. `314`  
B. `"314"`  
C. `int`  
D. `'34.0'`

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Check Yourself: Which Type 2?

What is the value of `type(314)` ?

A. `314`  
B. `"314"`  
C. `int`  
D. `'34.0'`

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Python String Formatting

<table style="font-size:1.0em;">
    <thead><tr>
        <th>Code</th>
        <th>Type</th>
        <th>Example</th>
        <th>Output</th>
    </tr></thead>
    <tbody>
    <tr>
        <td><code>%d</code></td>
        <td><code>int</code></td>
        <td><code>print("%d" % 50)</code></td>
        <td><code>50</code></td>
    </tr>
    <tr>
        <td><code>%f</code></td>
        <td><code>int</code></td>
        <td><code>print("%.2f" % 4.5)</code></td>
        <td><code>4.50</code></td>
    </tr>
    <tr>
        <td><code>%d</code></td>
        <td><code>str</code></td>
        <td><code>print("[%s]" % "mike")</code></td>
        <td><code>[mike]</code></td>
    </tr>
  </tbody>
</table>


```python
name = 'mike'
age = 45
wage = 10.5
print("%s is %d years old. He makes $%.2f/hr" % (name, age, wage) )
```

# Python F-String Interpolation

The `f` in front of the `""` tells Python to interpolate the `{}` in the string, replacing them with values of the variables.


```python
name = 'mike'
age = 45
wage = 10.559

print("%s is %d years old. He makes $%.2f/hr" % (name, age, wage) )

# f-string style
print(f"{name} is {age:d} years old. He makes ${wage:.2f}/hr")
```

# Watch Me Code 2

### Python String Formatting with inputs

- Inputs
- F-strings
- Formatting
- Alignment


# Check Yourself: Formatting 1

This Python statement yields which output?   
`print("%.1f" % 34)`


A. `34`  
B. `34.0`  
C. `$34`  
D. `$34.0` 

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)



# Check Yourself: Formatting 2

This Python code yields which output?   
```
mike = 10
print(f"{mike:.5f}")
```

A. `10`  
B. `10.0`  
C. `10.00000`  
D. `10.5` 

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)


# Programmatic Expressions

Programmatic Expressions contain **operators** and **operands**. They evaluate to a value, preserving type: 




```python
print(2 + 2)
print(2.0 + 2)
print("sh" + 'ip')
print('hi' + 2)
```

# Arithmetic Operators

<table style="font-size:1.2em;">
    <thead><tr>
        <th>Operator</th>
        <th>What it Does</th>
        <th>Example of Use</th>
    </tr></thead>
    <tbody>
    <tr>
        <td><code>+</code></td>
        <td>Addition or string concenation</td>
        <td><code>3 + 4 == 7</code></td>
    </tr>
    <tr>
        <td><code>-</code></td>
        <td>Subtraction</td>
        <td><code>4 - 3 == 1</code></td>
    </tr>
    <tr>
        <td><code>*</code></td>
        <td>Multiplication</td>
        <td><code>3 * 4 == 12</code></td>
    </tr>
    <tr>
        <td><code>/</code></td>
        <td>Division</td>
        <td><code>4 / 3 == 1.33333</code></td>
    </tr>
    <tr>
        <td><code>//</code></td>
        <td>Intger division (quotent)</td>
        <td><code>13 // 3 == 4</code></td>
    </tr>
    <tr>
        <td><code>%</code></td>
        <td>Modulo (remainder)</td>
        <td><code>13 % 3 == 1</code></td>
    </tr>
    <tr>
        <td><code>( )</code></td>
        <td>Force an order of operations</td>
        <td><code>2 * (3 + 4) == 14</code></td>
    </tr>
  </tbody>
</table>

# Check Yourself: Operators

What is the output of the following python code?
```
a = 10
b = 2
c = 1 + (a/b)
print(c)
```

A. `6`  
B. `5.5`  
C. `6.0`  
D. `5` 

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# End To End Example

### The Pay-Rate Calculator:

- Write a program to prompt for hourly rate, and hours worked for the week as inputs
- Then calculates the total pay as output. 
- Then prompts for tax rate as input, and outputs net pay.


# Conclusion Activity Exit Ticket

What is the value of: `type(int("1"+"4")/2)` ?

A. `float`   
A. `int`   
A. `7`   
A. `7.0`   


### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)
