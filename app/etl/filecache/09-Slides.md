# IST256 Lesson 09
## Dictionaries

- P4E Ch9


## Links

- Participation: [https://poll.ist256.com](https://poll.ist256.com)  (Sign in with *netid*@syr.edu and your SU Password.)
- Class Chat: [https://chat.ist256.com](https://chat.ist256.com)  (Microsoft Teams.)


# FEQT (Future Exam Questions Training) 1

What is the output of the following code?


```python
x = [1,3,5]
x.append(7)  # 1,3,5,7
x.insert(0,2) # 2,1,3,5,7
x.pop(-2) # 2,1,3,7
print(x)
```

A. `[1,3,5,7]`  
B. `[1,2,5,7]`  
C. `[2,1,3,7]`  
D. `[2,1,3,5]`  
 
## Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# FEQT (Future Exam Questions Training) 2

What is the output of the following code?


```python
x = [5,3,1]
y = [2,3]
z = x + y
z.sort()
print(z)
```

A. `[1,2,3,3,5]`  
B. `[1,2,3,5]`  
C. `[5,3,1,2,3]`  
D. `[5,3,1,2]`  
 
## Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Agenda

- Previous Homework! 


- Dictionaries as key-value pairs.
- Basic dictionary operations such as getting/setting keys and values
- Common dictionary use cases, such as representing complex objects.
- List of dictionary as an in-memory database of objects.
- Using the json library to load and save dictionaries to files. 


# Connect Activity

Question: A Python Dictionary is a   
A. `Immutable Sequence Type`  
B. `Mutable Mapping Type`  
C. `Mutable Sequence Type`  
D. `Immutable Mapping Type`
  
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Dictionaries

- The **dict** type is designed to store key-value pairs. In Python this is known as a **mapping type**.  
`font={'Name':'Arial','Size': 8}`
- Python dictionaries are **mutable** which means you can change the values of the keys after they have been set.
- Dictionary values are accessed by **key** not by **index**.  
`font['Name'] = 'Courier'`  


# Watch Me Code 1 

### Dictionary Basics:
- Create a dictionary
- Update its value
- Print it out
- `KeyError`


# Dictionary Methods

- Like **str** and **list**, the **dict** type has its own set of built-in functions. 
- https://docs.python.org/3/library/stdtypes.html#mapping-types-dict 
- Don't forget our helper functions `dir()` and `help()`


# Watch Me Code 2

### Dictionary Methods:
- Handling `KeyError`
- using `get()`  to avoid `KeyError`
- `values()`
- `keys()`
- delete a key with `del` 


# Check Yourself: Dictionaries 1

- What is the output on line 2?



```python
x = { 'a' : 'b', 'b' : 2, '2' : 6}
x['b']
```

A. `2`  
B.`'2'`  
C. `6`   
D. `KeyError`  

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Check Yourself: Dictionaries 2

- What is the output on line 2?



```python
x = { 'a' : 'b', 'b' : 2, '2' : 6}
x.get('d', 6)
x['d'] # <= KeyError
```

A. `2`  
B.`'2'`  
C. `6`   
D. `KeyError`  

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Dictionaries or Lists?

When do you use a Python **list** versus a **dict**?   

As a best practice:  

- **Lists** are for **multiple versions** or **collections** of the **same type**.   
Ex: Student GPA's  
`[3.4,2.8,4.0]`
- **Dictionaries** are for **single versions** or **records** of **different types**.  
Ex: One Student's Name, GPA and Major    
`{ 'Name' : 'bob', 'GPA' : 3.4 }`


# Python's List of Dictionary

#### For representing complex data structures…




```python
students = [     
    { 'Name':'bob','GPA':3.4 },   
    { 'Name':'sue','GPA':2.8 },  
    { 'Name':'kent','GPA':4.0 }  
]

#chaining
students[0]['Name']
```

# Watch Me Code 3 

### List of Dictionary:

- Using `type()` 
- chaining methods / operators to access values of complex types
- `KeyError` versus `IndexError`


# Check Yourself: List of Dict 1

Given the following Python code, match the Python Expression to it's answer:   
`s[0]['c']`



```python
s = [ { 'a':'bob','b':3.4 },   
      { 'a':'sue','b':2.8 },  
      { 'a':'kent','b':4.0 } ]

s[0]['c']
```

A. `3.4`  
B. `KeyError`  
C. `IndexError`  
D. `'sue'  

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Check Yourself: List of Dict 2

Given the following Python code, match the Python Expression to it's answer

`s[3]['a']`


```python
s = [ { 'a':'bob','b':3.4 },   
      { 'a':'sue','b':2.8 },  
      { 'a':'kent','b':4.0 } ]

s[0]['b']
```

A. `3.4`  
B. `KeyError`  
C. `IndexError`  
D. `'sue'  

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# JSON and Python Dictionaries

- JSON (**JavaScript Object Notation**) is a standard, human-readable  data format. It's a popular format for data on the web.
- JSON Can be easily converted to lists of dictionaries using Python's **json** module.
- Transferring a JSON string to Python is known as **de-serializing**. 
- Transferring Python to a JSON string is known as **serializing**. 
- **<font color='red'>This is easy to do in Python but challenging to do in most other languages.</font>**


# Watch Me Code 4 

- Let's look at JSON Data 
- `import json`
- Decode JSON Data
- Load into List of Dictionary
- Access data to obtain output


# End-To-End Example

### European Country Locator
- Load JSON data for Countries in Europe
- Input a country
- Output 
    - Region (Southern Europe)
    - Neighboring Countries

# Conclusion Activity : Exit Ticket

Assuming `z` is a list, `z['mike']` is a:

A. `KeyError`  
B. `IndexError`  
C. `TypeError`

