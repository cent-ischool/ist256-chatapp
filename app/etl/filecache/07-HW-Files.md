# Homework: Mass Email Marketing

## The Problem

You have been contracted by former energy company **Enron** to create a database of email addresses for "mass marketing" *ahem* ,*cough*: SPAMMING. You will get the emails for this "mass marketing" campaign from the email inboxes of the sales team, provided here.

- `enron-allen-inbox.txt`
- `enron-donohoe-inbox.txt`
- `enron-lay-inbox.txt`
- `enron-williams-inbox.txt`
- `enron-onemail-inbox.txt` ( a sample with just one email in it - helpful for testing)

### Run this cell to download the files you need to your computer.



```python
! curl https://raw.githubusercontent.com/mafudge/datasets/master/ist256/07-Files/enron-allen-inbox.txt -o enron-allen-inbox.txt
! curl https://raw.githubusercontent.com/mafudge/datasets/master/ist256/07-Files/enron-donohoe-inbox.txt -o enron-donohoe-inbox.txt
! curl https://raw.githubusercontent.com/mafudge/datasets/master/ist256/07-Files/enron-lay-inbox.txt -o enron-lay-inbox.txt
! curl https://raw.githubusercontent.com/mafudge/datasets/master/ist256/07-Files/enron-williams-inbox.txt -o enron-williams-inbox.txt
! curl https://raw.githubusercontent.com/mafudge/datasets/master/ist256/07-Files/enron-small-inbox.txt -o enron-small-inbox.txt
```

Your ultimate task is to provide a drop-down so the user of the program can select one of the 5 mailboxes. Upon running the interaction the program will:

 - read the selected mailbox file a line at a time
 - find any lines beginning with `From:`.
 - extract out the email address from the `From:` line.
 - use the `isEmail()` function (provided below) to ensure its a valid email address.
 - check to make sure its not an `enron.com` email address
 - print the valid non Enron email address
 - write the same thing you print to a file
 - If you read in `enron-allen-inbox.txt` you should write out `enron-allen-emails.txt`

## Approach:

This assignment is broken up into parts. We will use problem simplification to solve this problem.

- **You Code 2.1** we search the file a line at a time for lines beginning with `From:`
- **You Code 2.2** builds on 2.1. Specifically 1) Remove the `From:` 2) check to see if the remainder is an actual email, and 3) if its an email check to see if its an `enron.com` email. We only display emails not from Enron.
- **You Code 2.3** not only `print()` the emails but write them to a file.
- **You Code 2.4** final Program. Build an `@interact_manual` to allow the user to select the email inbox to process.



```python
def isemail(text):
    import re
    '''
    returns True if text is a valid email address
    '''
    return re.fullmatch("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", text) is not None
```


```python
#Tests
assert isemail("mafudge@syr.edu")==True
assert isemail("mafudge@mail.syr.edu")==True
assert isemail("mike.mafudge@syr.edu")==True
assert isemail("mike@")==False
assert isemail("@syr.edu")==False
assert isemail("m@syr")==False
assert isemail("msyr")==False
```

## Part 1: Problem Analysis

You will complete a problem analysis for the entire program.


### 1.1 Program Outputs

Describe your program outputs in the cell below. 




### 1.2 Program Inputs

List out the program inputs in the cell below.


   

### 1.3 The Plan (Algorithm)

Explain, as specifically as you can, without writing code, how the program works from input to output. Be detailed with your plan as you will need to turn it into code. 




## Part 2: Code Solution

You may write your code in several cells, but place the complete, final working copy of your code solution within this single cell below. Only the within this cell will be considered your solution. Any imports or user-defined functions should be copied into this cell. 


```python

```

### You Code 2.1 Extract From: lines

In this first part, read in the file a line at a time. For now, only use `enron-small-inbox.txt`. In this file and only print the lines which begin with `From:`

Here is the expected output from the file `enron-small-inbox.txt`
```
From: anchordesk_daily@anchordesk.zdlists.com
From: subscriptions@intelligencepress.com
From: prizemachine@feedback.iwon.com
From: louise.kitchen@enron.com
From: arsystem@mailman.enron.com
From: exclusive_offers@sportsline.com
From: Pizza Hut
```

**NOTE:** For this step just use the `enron-small-inbox.txt`


```python
# SOLUTION CELL 2.1

```

### You Code 2.2 Just Actual Emails and Outside the `enron.com` Domain:

In this next part, starting with the code you wrote in 2.1. for each `From:` line:
 - remove the `From:` from the line
 - check to see if the rest of the line is an email using `isemail()` 
 - check if the email is an `enron.com` email 
 - Only print if they satisfy those requirements. 

Here is the expected output from the file `enron-small-inbox.txt`
```
anchordesk_daily@anchordesk.zdlists.com
subscriptions@intelligencepress.com
prizemachine@feedback.iwon.com
exclusive_offers@sportsline.com
```

**NOTE:** For this step just use the `enron-small-inbox.txt`


```python
# SOLUTION CELL 2.2
# NOTE: required for checker to work
def isemail(text):
    import re
    return re.fullmatch("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", text) is not None

# Your Code Starts here

```

### You Code 2.3 Writing the valid emails to a file

In this final part, re-write your code so that after you print, you also write the email to a file. The trick here is:
- Input the name of the mailbox file: For example: `enron-small-inbox.txt` or `enron-williams-inbox.txt`, etc...
- Turning the input file name into the output file name. For example `enron-small-inbox.txt` into `enron-small-emails.txt`.
- Where in the code do you open the `enron-small-emails.txt` so it can be written to and also saves every email to the file.
- Keeping track of the number of emails it wrote to the file.

For example, here is the expected output from the file `enron-small-inbox.txt`

The contents of your `enron-small-emails.txt` should be:
```
anchordesk_daily@anchordesk.zdlists.com
subscriptions@intelligencepress.com
prizemachine@feedback.iwon.com
exclusive_offers@sportsline.com
```

To the console, we should see:

```
anchordesk_daily@anchordesk.zdlists.com
subscriptions@intelligencepress.com
prizemachine@feedback.iwon.com
exclusive_offers@sportsline.com

Wrote 4 emails to enron-small-emails.txt
```


**NOTE:** For this step you should `input()` the mailbox file name. That way the code checker can try a different file, such as `enron-lay-inbox.txt`


```python
# SOLUTION CELL 2.3
# NOTE: required for checker to work.
def isemail(text):
    import re
    return re.fullmatch("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", text) is not None

# Your code starts here

```

### You Code 2.4 Interact Manual

Re-write the final program as an `@interact_manual` the input widget should be a drop-down of the 5 available mailboxes from the top

**NOTE:** this code will be graded manually


```python
# SOLUTION CELL 2.4
from ipywidgets import interact_manual
mailfiles = ["enron-allen-inbox.txt","enron-donohoe-inbox.txt","enron-lay-inbox.txt","enron-williams-inbox.txt", "enron-small-inbox.txt"]


```
