# IST256 Lesson 10
## Data Analysis with Pandas, Part I


- Reading: Fudge: DataAnalysisWithPandas.ipynb (Intro, Part One)
- Reading 10 Minutes to Pandas: https://pandas.pydata.org/docs/user_guide/10min.html


## Links

- Participation: [https://poll.ist256.com](https://poll.ist256.com)  (Sign in with *netid*@syr.edu and your SU Password.)
- Class Chat: [https://chat.ist256.com](https://chat.ist256.com)  (Microsoft Teams.)


# Agenda

- Homework Solution
- Transitions...
- The Project
- What is Data Analysis?
- What is Pandas?


# Transitions

- You've learned the Python essentials 01 - 09
- The remaining 4 units 10 - 13 cover data analysis, visualization and data storytelling 
- Content was re-written and updated, there are no lab / hw videos.
- Labs, SmallGroup and HW are are examples of simple projects.


# The Project (49/250 points)

Build a data analysis as to tell a story with your data.

- P1: Data set selection. April 12th
- P2: Exploratory Data Analysis. April 29th 
- P3: Your data product w/ Interact. May 7th
- P4: Tell your story: Video demo your data product / share what you learned. May 7th

More Info: [https://ist256.com/syllabus/#project-p1-p4](https://ist256.com/syllabus/#project-p1-p4)

# Connect Activity

#### Question: 
The process of systematically applying techniques to evaluate data is known as ?  
A. Data Munging  
B. Data Analysis  
C. Data Science  
D. Data Pandas  

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Data Analysis:

- **What is it?**
    - Apply logical techniques to
    - Describe, condense, recap and evaluate Data and 
    - Illustrate Information  
        

- **Goals of Data Analysis:**  
    1. Discover useful information
    2. Provide insights
    3. Suggest conclusions
    4. Support Decision Making	


## Examples of Data Analysis:

- Which exam in IST256 has the lowest average?
- Does weather play a factor in student attendance?
- Which regions of the US experience lower death rates (visualization of a DA)
- Do students who answer the polls perform better on exams? (statistical analysis)

# What is pandas ?

- ***Pandas*** (Panel Data) is Python library to aid in performing **data analysis.** 
- It allows you to fetch data from a variety of sources and tabularize it.
- It Provides built-in data structures which simplify the manipulation and analysis of data sets. 
- We cannot teach you all things Pandas, we must focus on how it works, and the fundamentals.
- http://pandas.pydata.org/pandas-docs/stable/ 


# Pandas is the next theme...

... In a common thread.

- We learned about `list`s and reading files
- Then we learned about `dict`ionaries, `JSON` format and Python data structures, like `list[dict]`
- Now we will learn to load data into tables and manipulate the tabular data structures

# Pandas: Essential Concepts

- Before we can use it we must import it:  
  `import pandas as pd`
- A **Series** is a named Python list of values.
   `pd.Series(data=[50,90,100,45], name='Grade')`
- A **DataFrame** is table representation of your data. it is a `dict` of Series:  
  `pd.DataFrame({ 'customer': ['bob','ken','abby','jeane'] }, {'order': [50,90,100,45] })`


# Watch Me Code 1

### Pandas Basics
- Series
- DataFrame
- `loc[]` for accessing values
- Creating a DataFrame from a dict
- Select columns, Select rows with Boolean indexing


# Check Yourself: Series or DataFrame?

#### Match the code to the result. One result is a Series, the other a DataFrame
`df['Quarter']`

![image.png](image.png)  

A. `Series`   
B. `Data Frame`  
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Check Yourself: loc[]

#### Match the code to the result. One result is a Series, the other a DataFrame
![image.png](image.png)  
`df.loc[2,"Sold"]`  

A. `Q2`   
B. `Q3`  
C. `120`  
D. `90`  
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# Check Yourself: Boolean Index

#### Which rows are included in this Boolean index?
![image.png](image.png)  
`[ df['Sold'] < 110 ]`  
A. `0, 1, 2`  
B. `1, 2, 3`  
C. `0, 2`  
D. `0,1`  
### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

 # Loading Data using Pandas DataFrames
 
 - Pandas can load a wide variety of data into dataframes!
     - csv / excel / delimited files
     - database tables and queries
     - HTML tables on webpages
     - JSON data
     - API output
     - Big data file formats (feather, farquet, HDF5)
 - Once its in a DataFrame its easy to explore and manipulate using the same Pandas methods!

 # Explore your data after loading
 
 - `info()` - column information / data types
 - `describe()` - get statistics on numerical columns
 - `head(n=5)` view the FIRST `n` rows in the dataframe (defaults to 5)
 - `tail(n=5)` view the LAST `n` rows in the dataframe (defaults to 5)
 - `sample(n=1)` view a random `n` rows from the dataframe (defautls to 1)

# Watch Me Code 2

### Read in the Superhero Movie Dataset

https://raw.githubusercontent.com/mafudge/datasets/master/superhero/superhero-movie-dataset-1978-2012-header.csv

 - Explore the data with `info(), describe(), head()`
 - How many DC? Marvel? `value_counts()`
 - dropping NaN values
 - Highest Rated imdb movie? Lowest?


# Data Feature Engineering

- Sometimes what you need for your analysis is not available in the source data
- But it can be derived from the given data, or through the addition of other data.
- Engineering data features is an important facet of data analysis.


# Watch Me Code 3

### Data Feature Engineering 

https://raw.githubusercontent.com/mafudge/datasets/master/superhero/superhero-movie-dataset-1978-2012-header.csv

- Title with Highest Box office Gross
    - Ticket prices vary year to year.,
- Title with best opening weekend attendance.
    - Is the attendance better because there are simply more eligible people to go?
- Engineering the columns we need to answer the questions!


# End-To-End Example

### Building a Data Product from `superhero2.csv`

- UI to search for a title
- Select a range for the Composite score.
- Output the Results


# Conclusion Activity : One Question Quiz

For the following dataframe, `df`

<table style="font-size:1.0em;">
    <thead><tr>
        <th>a</th>
        <th>b</th>
        <th>c</th>
    </tr></thead>
    <tbody>
    <tr>
        <td>1</td>
        <td>x</td>
        <td>y</td>
    </tr>
    <tr>
        <td>3</td>
        <td>w</td>
        <td>y</td>
    </tr>
    <tr>
        <td>5</td>
        <td>q</td>
        <td>z</td>
    </tr>
    </tbody>
</table>

what is: `df[ df['c'] =='z' ]['a']`   

A. `1`  
B. `3`  
C. `5`  
D. `a`  


### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)
