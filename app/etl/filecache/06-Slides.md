# IST256 Lesson 06
## Strings

- P4E Ch6


## Links

- Participation: [https://poll.ist256.com](https://poll.ist256.com)  (Sign in with *netid*@syr.edu and your SU Password.)
- Class Chat: [https://chat.ist256.com](https://chat.ist256.com)  (Microsoft Teams.)


# An Algorithm: 

    A. Helps you plan the code before your write it
    B. Should be written before you code
    C. Should be detailed enough that a skilled programmer can convert it to code
    D. All of the above

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)



# Good and Bad Algos:

    steps for get_paint_info function:
        
    GOOD:
    if paint is "everyday" then
        price is 19.95 and coverage is 320
    else if paint is "premium"
        price is ....
            
    BAD:
    figure out price and coverage base in paint type


# Functions

    def something(foo, bar):
       return baz

What is the input?

    A. foo
    B. bar
    C. baz
    D. something

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)


# Agenda

Homework 05

- Quick Review of the Solution

Strings
- Strings are immutable sequence of characters.
- Index and Slice notation for retrieving sub-strings.
- Built-in string functions to perform operations on strings.
- Techniques for parsing and tokenizing string data.
- How to sanitize input with string functions.


# FEQT (Future Exam Questions Training) 1

What is the output of the following code?



```python
def doit(a, b):
    return f"{a}{b}"

b = 4
a = 3
z = doit(b, a)
print(z)
```

 ``` 
  A. 34 
  B. 43
  C. Error (NameError)  
  D. 6 
 ```
 ### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)


# FEQT (Future Exam Questions Training) 2

Given the following input `4` what is the output?



```python
x = int(input())
z = 0
for i in range(x):
    z = z + i
print(z)
```

A. 3  
B. 4  
C. 6  
D. 10  
 
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)


# FEQT (Future Exam Questions Training) 3

Given the following input `4` what is the output?



```python
def x(a,b):
    return b

w = 4
y = 2
for i in range(4):
    0 1 2 3 
    t = x(y, i) x(2,0) t==0
                x(2,1) t==1
                x(2,2) t==2
                x(2,3) t==3
print(t)
```


      Cell In[2], line 7
        0 1 2 3
          ^
    SyntaxError: invalid syntax



A. 8  
B. 6  
C. 4  
D. 2  
 
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)


# Strings are Sequences of Characters

- **Strings** are index able sequences of characters. 
- The characters inside the string are **immutable**.
![image.png](image.png)
- **Example:**
    - **<font color='green'> Name = 'Fudge'</font>**
    - **<font color='green'>len(Name) == 5</font>**
- Immutable means we can’t change part of it:
    - **<font color='red'>Name[1] = 'u'</font>**

# Slice Notation

- **Slice Notation** is used to extract a substring.
![image.png](image.png)
- **Examples:**
    - **<font color='green'>Name[0:2] == 'Fu'</font>**
    - **<font color='green'>Name[2:5] == 'dge'</font>**
    - **<font color='green'>Name[:4] == 'Fudg'</font>**
    - **<font color='green'>Name[:] == 'Fudge'</font>**
    - **<font color='green'>Name[1:-1] == 'udg</font>**




# Check Yourself: String Slices 1

####  Match each string slice to its value for this string:
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`x ='orange'`

**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; x[1:6]**  

   &nbsp;&nbsp; `A. 'ang'`    
   &nbsp;&nbsp; `B. 'rang'`   
   &nbsp;&nbsp; `C. 'range'`
   
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)
   

# Check Yourself: String Slices 2

####  Match each string slice to its value for this string:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`x ='orange'`

**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; x[2:-1]**    

   &nbsp;&nbsp; `A. 'ang'`    
   &nbsp;&nbsp; `B. 'rang'`     
   &nbsp;&nbsp; `C. 'range'`  
   
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)
   

# String functions:

- **Built In** String Functions: 
    https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str 
    - `dir(str)`
    - `help(str.upper)`
- The Python String Library:
    https://docs.python.org/3/library/string.html
    - You must `import String` before you can use them.

# Watch Me Code 1

### Yes or No?
- Write a function to accept a variety of inputs as "yes" or "no"
- **<font color='green'> "yes" <span>&#8594;</span>  "y", "Y", "YES", "Yes" etc… </font>**
- **<font color='green'>"no" <span>&#8594;</span> "n", "N", "NO", "No", etc…</font>**


# Check Yourself: Code Trace 1

What is the value of the variable y on line 2? 


```python
x = "Mike"
y = x.upper().replace("I","K")
y
```




    'MKKE'



A. `'Miie'`  
B. `'MKKE'`   
C. `'MIIE'`  
D. `'Mkke'`  
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# String Tokenization and Parsing

- **Tokenization**  is the process of breaking up a string into words, phrases, or symbols. 
    - Tokenize a sentence into words.
    - `"mike is here"` becomes the iterable  `['mike','is','here']`
- **Parsing** is the process of extracting meaning from a string. 
    - Parse text to a numerical value or date.
    - `int('45')` becomes `45`




# Watch Me Code 2

Given a string of digits: e.g. `'12 45 90'`
1. Tokenize into individual strings
2. Parse into integers
3. Add them up!


# Check Yourself: Code Trace 2

What is the output of this program? 


```python
text = "This is mike"
for word in text.split():
    print(word[0], end='')
```

    Tim

A. `This`  
B. `T`  
C. `Tim`  
D. `mike`
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# End-To-End Example

**Parsing Tweets**

Let write a program which takes a tweet as input and extracts out the hashtags and mentions.

`#hashtag` `@mention`

### Structure of a python program

1. imports
2. user-defined function
3. main code or interact function which executes the main code


# Conclusion Activity : One Question Challenge


What is the value of:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`x[4:8]`  
When **`x = 'Syracuse'`?

A. `'Syracuse'`  
B. `'cuse'`  
C. `'Syra'`  
D. `'acuse'`  

