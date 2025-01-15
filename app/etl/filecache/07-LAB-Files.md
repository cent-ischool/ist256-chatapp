# In-Class Coding Lab: Files

The goals of this lab are to help you to understand:

- Reading data from a file all at once or one line at a time.
- Searching for data in files
- Parsing text data to numerical data.
- How to build complex programs incrementally.

## Parsing Email Headers

For this lab, we will write a program to read data from a mailbox file like `mbox-tiny.txt` or `mbox-short.txt`. These files contain raw email data, and in that data are attributes like who the message is To, From, the subject and SPAM confidence number for each message, like this:

`X-DSPAM-Confidence:0.8475`

Our goal will be to find each of these lines in the file, and extract the confidence number (In this case `0.8475`), with the end-goal of calculating the average SPAM Confidence of all the emails in the file. 

### Getting the files we need

Run this code to fetch the files we need for this lab. This linux code downloads them from the internet and saves them to your folder on jupyterhub.



```python
! curl https://raw.githubusercontent.com/mafudge/datasets/master/ist256/07-Files/mbox-tiny.txt -o mbox-tiny.txt
! curl https://raw.githubusercontent.com/mafudge/datasets/master/ist256/07-Files/mbox-short.txt -o mbox-short.txt
```

### Reading from the file

Let's start with some code to read the lines of text from `CCL-mbox-tiny.txt` this code reads the contents of the file one line at a time and prints those contents back out. 

- `f.readlines()` reads the file line-by-line. NOTE: We could read this file all at once, but it would be more difficult to process that way.
- `line.strip()` is required to remove the end-line character from each line since the `print()` function includes one already.


```python
filename = "mbox-tiny.txt"
with open(filename, 'r') as f:
    for line in f.readlines():
        print(line.strip())

```

### 1.1 You Code: Debug 

The following code should print the number of lines of text in the file `'mbox-tiny.txt`. There should be **332** lines. Debug this code to get it working. 

There should be **332** lines.



```python
# TODO debug this code to print the number of lines in the file
line_count = 0
filename = "mbox-tiny.txt"
with open(filename, 'r')
    for line in f.readlines():
        line_count = 1

print("there are {line_count} lines in the file")
```


### Finding the SPAM Confidence lines

Next, we'll focus on only getting lines addressing lines in the mailbox file that start with `X-DSPAM-Confidence:`. We do this by including an `if` statement inside  the `for` loop. 

**This is a very common pattern in computing used to search through massive amouts of data.**



Rather than print ALL 332 lines in `mbox-tiny.txt` we only print lines that begin with `X-DSPAM-Confidence:` There are only **5** such rows in this file.


```python
filename = "mbox-tiny.txt"
with open(filename, 'r') as f:
    for line in f.readlines():
        if line.startswith("X-DSPAM-Confidence:"):
            print(line.strip())

```

### Parsing out the confidence value

The final step is to figure out how to parse out the confidence value from the string.  

For example for the given line: `X-DSPAM-Confidence: 0.8475` we need to get the value `0.8475` as a float.

The strategy here is to use the string `.replace()` method to replace `X-DSPAM-Confidence:` with an empty string`""`. After we do that we can call the `float()` function to parse the string number to a `float`. 

### 1.2 You Code
Write code to parse the value `0.8475` from the text string `'X-DSPAM-Confidence: 0.8475'`.


```python
# TODO: Write code here
line = 'X-DSPAM-Confidence: 0.8475'

```

## Putting it all together

Now that we have all the working parts, let's put it all together.

    0.  use the file named 'mbox-short.txt' 
    1.  line count is 0
    2.  total confidence is 0
    3.  open mailbox file
    4.  for each line in file
    5.  if line starts with `X-DSPAM-Confidence:`
    6.     remove `X-DSPAM-Confidence:` from line and convert to float
    7.     increment line count
    8.     add spam confidence to total confidence
    9.  print average confidence (total confidence/line count)
    
    
### 1.3  You Code 



```python
#TODO Write Code here       

```

## Who are these emails from?

Now that you got it working once, let's repeat the process to discover who sent each email. The approach is similar to the spam confidence example but instead we search for lines that start with `From:`. For example:  

`From: stephen.marquard@uct.ac.za`

To extact the email we remove the `From: ` portion from the line.


    0.  use the file named 'mbox-short.txt' 
    1.  open mailbox file
    2.  for each line in file
    3.  if line starts with `From:`
    4.     remove `From:` from line and strip out any remaining whitespace
    5.     print email


### 1.4 You code



```python
#TODO Write Code here 

```
