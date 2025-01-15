# In-Class Coding Lab: Strings

The goals of this lab are to help you to understand:

- String slicing for substrings
- How to use Python's built-in String functions in the standard library.
- Tokenizing and Parsing Data
- How to create user-defined functions to parse and tokenize strings


# Strings

## Strings are immutable sequences

Python strings are immutable sequences.This means we cannot change them "in part" and there is impicit ordering. 

The characters in a string are zero-based. Meaning the index of the first character is 0.

We can leverage this in a variety of ways.

For example:


```python
something = input("Enter something: ")
print ("You typed:", something)
print ("We can extract parts of the string:")
print ("number of characters:", len(something) )
print ("First character is:", something[0])
print ("Last character is:", something[-1])

print ("They are sequences, so we can iterate over them:")
print ("Printing one character at a time: ")
for ch in something:
    print(ch) # print a character at a time!
```

## Slices as substrings

Python lists and sequences use **slice notation** which is a clever way to get a substring from a given string.

Slice notation requires two values: A start index and the end index. The substring returned starts at the start index, and *ends at the position before the end index*. It ends at the position *before* so that when you slice a string into parts you know where you've "left off". 

For example:


```python
state = "Mississippi"
print (state[0:4])          # Miss
print (state[4:len(state)]) # issippi
```

In this next example, play around with the variable `split` adjusting it to how you want the string to be split up. Re run the cell several times with different values to get a feel for what happens.


```python
state = "Mississippi"
split = 4   # TODO: play around with this number
left = state[0:split]
right = state[split:len(state)]
print(left, right)
```

### Slicing from the beginning or to the end

If you omit the begin or end slice, Python will slice from the beginnning of the string or all the way to the end. So if you say `x[:5]` its the same as `x[0:5]`

For example:


```python
state = "Ohio"
print(state[0:2], state[:2]) # same!
print(state[2:len(state)], state[2:]) # same

```

### 1.1 You Code

Split the string  `"New Hampshire"` into two sub-strings one containing `"New"` the other containing `"Hampshire"` (without the space).


```python
## TODO: Write code here

```

## Python's built in String Functions

Python includes several handy built-in string functions (also known as *methods* in object-oriented parlance). To get a list of available functions, use the `dir()` function on any string variable, or on the type `str` itself.



```python
dir(str)
```

Let's suppose you want to learn how to use the `count` function. There are 2 ways you can do this.

1. search the web for `python 3 str count` or
1. bring up internal help `help(str.count)` 

Both have their advantages and disadvanges. I would start with the second one, and only fall back to a web search when you can't figure it out from the Python documenation. 

Here's the documentation for `count`


```python
help(str.count)
```

You'll notice in the help output it says S.count() this indicates this function is a method function. this means you invoke it like this `variable.count()`.

### 1.2 You Code

Try to use the count() function method to count the number of `'i'`'s in the string `'Mississippi`:


```python
#TODO: use state.count
state = 'Mississippi'
```

### TANGENT: The Subtle difference between function and method.

You'll notice sometimes we call our function alone, other times it's attached to a variable, as was the case in previous example. When we say `state.count('i')` the period (`.`) between the variable and function indicates this function is a *method function*. The key difference between a the two is a method is attached to a variable. To call a method function you must type `variable.function()` whereas when you call a function its just `function()`. The variable associated with the method call is usually part of the function's context.

Here's an example:


```python
name = "Larry"
# a function call len(name) stands on its own. Gets length of 'Larry'
print( len(name) )

# a method call name.__len__()  does the names thing for its variable 'Larry'
print( name.__len__() ) 
```

### 1.3 You Code

Try to figure out which built in string method to use to accomplish this task.

Write some code to find the text `'is'` in some text. The program shoud output the first position of `'is'` in the text. 

Examples:

```
When: text = 'Mississippi' then position = 1
When: text = "This is great" then position = 2
When: text = "Burger" then position = -1
```

Again: DO NOT WRITE your own function, use `dir(str)` then the `help()` function to figure out which built-in string method should be used to accomplish this task.


```python
# workspace for using dir() and help()
```


```python
# TODO: Write your code here
text = input("Enter some text: ")

```

### 1.4 You Code: 

**Is that a URL?**

Let's write a user-defined function called `isurl()` which when input any `text` sting will return `True` when the `text` is a URL. [https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL). 

Here is the strategy for the function:

    - use build in string method `startswith()`
    - when `text` starts with `http://` or `https://` then the `text` is a url.
    - return True or False


The function stub and tests have been written for you. All you need to do is implement the function body.



```python
def isurl(text):
    # TODO implement function body here
    
```


```python
## TESTS: three test cases
text = "http://www.syr.edu"
expect = True
actual = isurl(text)
print(f"when text={text} EXPECT={expect} ACTUAL={actual}")
assert expect == actual

text = "https://www.syr.edu"
expect = True
actual = isurl(text)
print(f"when text={text} EXPECT={expect} ACTUAL={actual}")
assert expect == actual

text = "www.syr.edu"
expect = False
actual = isurl(text)
print(f"when text={text} EXPECT={expect} ACTUAL={actual}")
assert expect == actual
```

# Spliting text strings into Iterable Tokens


The `split()` string method allows us to take a string and split it into smaller strings. Each smaller string is now an iterable which means we can `for` loop over the collection.

The code sample below splits `text` into `words`. The default behavior of `split()` is to tokenize the string on whitespace.

We can then iterate over the tokens (in this case `words`) using a `for` loop.


```python
text = "this is a test"
words = text.split()
for word in words:
    print(word)
```

This next sample demonstrates you can `split()` on any token, not just whitespace. Here we have `text` with each grade separated by a comma `,` we `split(',')` to create a list of grades which we then check to see which grades are in the "A" range (A, A+, A-) by checking to see if the `grade.startswith("A")`


```python
acount=0
text = "A,B,A+,C-,D,A-,B+,C"
grades = text.split(',')
for grade in grades:
    print(grade)
    if grade.startswith("A"):
        acount +=1

print("Grades in A range: ", acount)
```

## Putting it all together: Extracting all URL's from text. 

Let's combine the `.split()` method with our own `isurl()` function to write a program which will extact all URL's from the input text. You will be given the alogorithm and be expected to write the code.

INPUT: text
OUTPUT: print each URL in the text:


ALGORITHM / STRATEGY:

    input the text
    split the text into tokens on space (let's call these words)
    for each word in the words
        if the word is a url
            print word
            
            
Example run:

    Enter text: Twitter https://twitter.com and Facebook https://facebook.com are social media sites. But the SU website
    https://syr.edu is not.
    EXTRACTED URLS:
    - https://twitter.com
    - https://facebook.com 
    - https://syr.edu 
    

### 1.5 You Code


```python
# TODO Write code here.

```
