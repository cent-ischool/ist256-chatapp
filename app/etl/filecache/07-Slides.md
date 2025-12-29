# IST256 Lesson 07
## Files

- P4E Ch7

## Links

- Participation: [https://poll.ist256.com](https://poll.ist256.com)  (Sign in with *netid*@syr.edu and your SU Password.)
- Class Chat: [https://chat.ist256.com](https://chat.ist256.com)  (Microsoft Teams.)


# Agenda

### Exam 1: Still grading - update next Monday!

### Go Over Homework  H06

### New Stuff
- The importance of a persistence layer in programming.
- How to read and write from files.
- Techniques for reading a file a line at a time. 
- Using exception handling with files.


# FEQT (Future Exam Questions Training) 1

What is the output of the following code when `berry` is input on line `1`?


```python
x = input()
if x.find("rr") != -1:
    y = x[1:]
else:
    y = x[:-1]
print(y)
```

A. erry   
B. berr  
C. berry  
D. bey   
 
## Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# FEQT (Future Exam Questions Training) 2

What is the output of the following code when `mike is cold` is input on line `1`?


```python
x = input()
y = x.split()
w = ""
for z in y:
    w = w + z[0]
print(w)
```

A. iic   
B. ike  
C. mic  
D. iso   
 
## Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# FEQT (Future Exam Questions Training) 3

What is the output of the following code when `tony` is input on line `1`?


```python
x = input()
x = x + x
x = x.replace("o","i")
x = x[:5]
print(x)
```

A. tony   
B. tiny  
C. tinyt  
D. tonyt   
 
## Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Connect Activity

Which of the following is not an example of secondary (persistent) memory?  
A. `Flash Memory`  
B. `Hard Disk Drive (HDD)`  
C. `Random-Access Memory (RAM)`  
D. `Solid State Disk (SSD)`  


### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)


# Files == Persistence

- Files add a **Persistence Layer** to our computing environment where we can store our data  **after the program completes**. 
- **Think: Saving a game's progress or saving your work!**
- When our program **Stores** data, we open the file for **writing**.
- When our program **Reads** data, we open the file for **reading**.
- To read or write a file we must first **open** it, which gives us a special variable called a **file handle**. 
- We then use the **file handle** to read or write from the file.
- The **read()** function reads from the **write()** function writes to the file through the file handle. 

# Reading From a File

Two approaches... that's it!


```python
# all at once
with open(filename, 'r') as handle:
    contents = handle.read()
    
# a line at a time
with open(filename, 'r') as handle:
    for line in handle.readlines():
        do_something_with_line
```

# Writing a To File



```python
# write mode
with open(filename, 'w') as handle:
    handle.write(something)
    
# append mode
with open(filename, 'a') as handle:
    handle.write(something)
```

# Watch Me Code 1

### Let’s Write two programs. 
- Save a text message to a file.
- Retrieve the text message from the file.


# Check Yourself: Which line 1

- Which line number creates the file handle?



```python
a = "savename.txt"
with open(a,'w') as b:
    c = input("Enter your name: ")
    b.write(c)
```

A. `1`  
B. `2`   
C. `3`   
D. `4`
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Watch Me Code 2

Common patterns for reading and writing more than one item to a file.
- Input a series of grades, write them to a file one line at a time.
- Read in that file one line at a time, print average.


# Check Yourself: Which line 2

- On which line number does the file handle no longer exist?


```python
with open("sample.txt","r") as f:
    for line in f.readlines():
        print(line)
f.read()
```

A. `1`  
B. `2`   
C. `3`   
D. `4`
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Your Operating System and You

- Files are stored in your **secondary memory** in **folders**. 
- When the python program is in the **same** folder as the file, **no path is required**.
- When the file is in a **different** folder, **a path is required**. 
- **Absolute paths** point to a file starting at the root of the hard disk.
- **Relative paths** point to a file starting at the current place on the hard disk.


# Python Path Examples

<table style="font-size:1.0em;">
    <thead><tr>
        <th>What</th>
        <th>Windows</th>
        <th>Mac/Linux</th>
    </tr></thead>
    <tbody>
    <tr>
        <td><code> File in current folder </code></td>
        <td> "file.txt" </td>
        <td> "file.txt"</td>
    </tr>
    <tr>
        <td><code> File up one folder from the current folder </code></td>
        <td> "../file.txt"</td>
        <td> "../file.txt"</td>
    </tr>
    <tr>
        <td><code> File in a folder from the current folder </code></td>
        <td> "folder1/file.txt" </td>
        <td> "folder1/file.txt" </td>
    </tr>
    <tr>
        <td><code> Absolute path to file in a folder</code></td>
        <td> "C:/folder1/file.txt" </td>
        <td> "/folder1/file.txt"</td>
    </tr>
  </tbody>
</table>

# Check Yourself: Path

### - Is this path relative or absolute?


      "/path/to/folder/file.txt"
      
A. `Relative`  
B. `Absolute`  
C. `Neither`  
D. `Not sure`  

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)


# Handling Errors with Try…Except

- I/O is the ideal use case for exception handling.
- Don't assume you can read a file!
- Use try… except!
 


```python
try:
    file = 'data.txt'
    with open(file,'r') as f:
        print( f.read() )
except FileNotFoundError:
    print(f"{file} was not found!")
```

#  End-To-End Example (Pre-Recorded)

#### How Many Calories in that Beer?

Let's write a program to search a data file of 254 popular beers. Given the name of the beer the program will return the number of calories.

Watch this here:
https://youtu.be/s-1ToO0dJIs


#  End-To-End Example

#### A Better Spell Check

In this example, we create a better spell checker than the one from small group.

- read words from a file
- read text to check from a file.


# Conclusion Activity : One Question Challenge

What is wrong with the following code:


```python
file = "a.txt"
with open(file,'w'):
    file.write("Hello")
```

A. `No file handle`  
B. `Cannot write - file opened for reading`  
C. `File a.txt does not exist`  
D. `Nothing is wrong!`  

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)
