# Homework: US Senator Lookup

## The Problem

Let's write a program similar to this unit's End-To-End Example. Instead of European countries this program will provide a drop-down of US states. When a state is selected, the program should display the US senators for that state.

What information Should you display? Here is a sample of the 2 senators from the State of `NY`:

## Sen. Charles “Chuck” Schumer [D-NY]

    Senior Senator for New York
    PARTY: Democrat
    PHONE: 202-224-6542
    WEBSITE: https://www.schumer.senate.gov
    CONTACT: https://www.schumer.senate.gov/contact/email-chuck
    
 ## Sen. Kirsten Gillibrand [D-NY]

    Junior Senator for New York
    PARTY: Democrat
    PHONE: 202-224-4451
    WEBSITE: https://www.gillibrand.senate.gov
    CONTACT: https://www.gillibrand.senate.gov/contact/email-me


## Approach:

This assignment is broken up into parts. We will use problem simplification to solve this problem and take a bottom up approach, making the components, then assembling them together.

- **You Code 2.1** Copy the `deserialize_json(0` function from small group. In this part you will write tests.
- **You Code 2.2** Write a `dedupe_states()` function deduplicate states from the deserialized JSON. 
- **You Code 2.3** Write a text-only version of the program. input a state, show senators form that state.
- **You Code 2.4** Write an interact versio of the program: dropdown list to select a state, then display senator. 

Since we are taking a bottom up approach, **hold off on completing part 1, until you are on step 2.3**

### This Code will fetch the current US Senators from the web and save the results to a `US-Senators.json` file.

Run this code to get the "latest" information about US Senators.


```python
import requests
import json 
file='US-Senators.json'
senators = requests.get('https://www.govtrack.us/api/v2/role?current=true&role_type=senator').json()['objects']
with open(file,'w') as f:
    f.write(json.dumps(senators))
    print(f"Saved: {file}")
```

## Part 1: Problem Analysis

You will complete a problem analysis for the entire program. **Since we are using the bottom-up approach, do not attempt until step 2.3**


### 1.1 Program Outputs

Describe your program outputs in the cell below. 




### 1.2 Program Inputs

List out the program inputs in the cell below.




### 1.3 The Plan (Algorithm)

Explain, as specifically as you can, without writing code, how the program works from input to output. Be detailed with your plan as you will need to turn it into code. 




## Part 2: Code Solution

You may write your code in several cells, but place the complete, final working copy of your code solution within this single cell below. Only the within this cell will be considered your solution. Any imports or user-defined functions should be copied into this cell. 

### You Code 2.1: Write tests for `deserialize_json()` function.

We wrote the `deserialize_json()` function in Small Group. So in this section you will write tests specific to the `US-Senators.json` file. NOTE: these tests will help you to extract the information you need later to write the program.

Specifics you must test for:

- Senator's party: example=Republican
- Senator's state: example=NY
- Senatory's birthday: example=1954-05-29
- Senator's contact_form: example= https://www.lankford.senate.gov/contact/email

I suggest opening the `US-Senators.json` in the Jupyterhub file preview and picking on a senator for your tests. Know the index of your senator. 

For each test, print the expected and actual tested value. To pass the automated code checks, your variable name must be `senators`.


Also you should `assert` the value under test, comparing expected to actual. See examples from small group for details.



```python
# SOLUTION CELL 2.1
def deserialize_json(jsonfile: str) -> any:
    import json
    with open(jsonfile, "r") as f:
        data = json.load(f)
        return data


# Write Test Code Below Here

```

### You Code 2.2: Write a `dedupe_states()` function deduplicate states from the deserialized JSON. 

Next we need to write a function to dedupe the states. Algorithmically, this will be similar to the `dedupe()` function we wrote previously, only we must retrieve the state from the each senator's 'state' key (which you figured out how to do in 2.1).

The input will be the list of `senators` the output will be a list of state codes, like `["NY","OH"]` in alphabetical order.

Here's the docstring:  

`dedupe_states(senators: list[dict]) -> list[str]`


The test has been written for you. If you're not getting 50 states back from `dedupe_states` something is not correct. 


```python
# SOLUTION CELL 2.2


```


```python
# Tests for 2.2
deduped_states = dedupe_states(senators)
expect_state_count = 50 # There are 50 states in the US
actual_state_count = len(deduped_states)
print(f"For deduped senator states, expect={expect_state_count} actual={actual_state_count}")
assert expect_state_count == actual_state_count
expect_ny_count = 1
actual_ny_count = deduped_states.count("NY")
print(f"For deduped senator states NY, expect={expect_ny_count} actual={actual_ny_count}")
assert expect_state_count == actual_state_count
```

### You Code 2.3 Write final program

Now that we have the components, its time to USE them to solve the original problem, assembing our components through a bottom-up appoach.

The Program should:

 - Read in and deserialize `US-Senators.json`
 - For a user input state in 2-character format, e.g "PA", display the following for each matching senator 
   - Name
   - Description
   - Party
   - Phone
   - Website
   - Contact Form
 - If the user enters an invalid state code like "XY" print out an error message.

Before you Write 2.3, go back to **Part 1: Problem Analysis** and complete your INPUT, OUTPUT, and STEPS sections!


```python
# SOLUTION CELL 2.3
# Copy your deserialize_json() function here


# Copy your dedupe_states() function here


# On with the MAIN PROGRAM


```

### You Code 2.4 Ipywidgets

Let's re-write the code as an `@interact_manual` You will need one input widget your list of deduplicated states. 

This solution will be checked manually by your instructor


```python
# SOLUTION CELL 2.4


```
