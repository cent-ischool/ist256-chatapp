# In-Class Coding Lab: Data Analysis with Pandas

In this lab, we will perform a **data analysis** on the **RMS Titanic** passenger list. The RMS Titanic is one of the most famous ocean liners in history. On April 15, 1912 it sank after colliding with an iceberg in the North Atlantic Ocean. To learn more, read here: https://en.wikipedia.org/wiki/RMS_Titanic 

Our goal today is to perform a data analysis on a subset of the passenger list. We're looking for insights as to which types of passengers did and didn't survive. Women? Children? 1st Class Passengers? 3rd class? Etc. 

I'm sure you've heard the expression often said during emergencies: "Women and Children first" Let's explore this data set and find out if that's true!

Before we begin you should read up on what each of the columns mean in the data dictionary. You can find this information on this page: https://www.kaggle.com/c/titanic/data 


## Loading the data set

First we load the dataset into a Pandas `DataFrame` variable. The `sample(10)` method takes a random sample of 10 passengers from the data set.


```python
import pandas as pd
import numpy as np

# this turns off warning messages
import warnings
warnings.filterwarnings('ignore')

passengers = pd.read_csv('https://raw.githubusercontent.com/mafudge/datasets/master/ist256/12-pandas/titanic.csv')
passengers.sample(10)
```

## How many survived?

One of the first things we should do is figure out how many of the passengers in this data set survived. Let's start with isolating just the `'Survivied'` column into a series:


```python
passengers.head(10)
```


```python
passengers['Survived'].sample(10)
```

There's too many to display so we just display a random sample of 10 passengers. 

- 1 means the passenger survivied
- 0 means the passenger died

What we really want is to count the number of survivors and deaths. We do this by querying the `value_counts()` of the `['Survived']` column, which returns a `Series` of counts, like this:


```python
passengers['Survived'].value_counts()
```

Only 342 passengers survived, and 549 perished. Let's observe this same data as percentages of the whole. We do this by adding the `normalize=True` named argument to the `value_counts()` method.


```python
passengers['Survived'].value_counts(normalize=True)
```

**Just 38% of passengers in this dataset survived.**

### 1.1 You Code

**FIRST** Write a Pandas expression to display value counts of males and female passengers using the `Sex` variable:


```python
# todo write code here

```

### 1.2 You Code 

**NEXT** Write a Pandas expression to display male /female passenger counts as a percentage of the whole number of passengers in the data set.


```python
# todo write code here

```

If you got things working, you now know that **35% of passengers were female**.

## Who survivies? Men or Women?

We now know that 35% of the passengers were female, and 65% we male. 

**The next thing to think about is how do survivial rates affect these numbers? **

If the ratio is about the same for surviviors only, then we can conclude that your **Sex** did not play a role in your survival on the RMS Titanic. 

Let's find out.


```python
survivors = passengers[passengers['Survived'] ==1]
survivors['PassengerId'].count()
```

Still **342** like we discovered originally. Now let's check the **Sex** split among survivors only:


```python
survivors['Sex'].value_counts()
```

WOW! That is a huge difference! But you probably can't see it easily. Let's represent it in a `DataFrame`, so that it's easier to visualize:


```python
sex_all_series = passengers['Sex'].value_counts()
sex_survivor_series = survivors['Sex'].value_counts()
data = {'AllPassengers': sex_all_series, 'SurvivorsOnly': sex_survivor_series }
sex_comparision_df = pd.DataFrame(data)
sex_comparision_df['SexSurvivialRate'] = sex_comparision_df['SurvivorsOnly'] / sex_comparision_df['AllPassengers']
sex_comparision_df
```

 **So, females had a 74% survival rate. Much better than the overall rate of 38%**
 
We should probably briefly explain the code above. 

- The first two lines get a series count of all passengers by Sex (male / female) and count of survivors by sex
- The third line creates a Pandas DataFrame. Recall a pandas dataframe is just a dictionary of series. We have two keys 'AllPassengers' and 'Survivors'
- The  fourth line creates a new column in the dataframe which is just the survivors / all passengers to get the rate of survival for that Sex.

## Feature Engineering: Adults and Children

Sometimes the variable we want to analyze is not readily available, but can be created from existing data. This is commonly referred to as **feature engineering**. The name comes from machine learning where we use data called *features* to predict an outcome. 

Let's create a new feature called `'AgeCat'` as follows:

- When **Age** <=18 then 'Child'
- When **Age** >18 then 'Adult'

This is easy to do in pandas. First we create the column and set all values to `np.nan` which means 'Not a number'. This is Pandas way of saying no value. Then we set the values based on the rules we set for the feature.


```python
passengers['AgeCat'] = np.nan # Not a number
passengers['AgeCat'][ passengers['Age'] <=18 ] = 'Child'
passengers['AgeCat'][ passengers['Age'] > 18 ] = 'Adult'

# take a sample to show, Check out the new "AgeCat" column
passengers.sample(10)
```

Let's get the count and distrubutions of Adults and Children on the passenger list.


```python
passengers['AgeCat'].value_counts()
```

And here's the percentage as a whole:


```python
passengers['AgeCat'].value_counts(normalize=True)
```

So close to **80%** of the passengers were adults. Once again let's look at the ratio of `AgeCat` for survivors only. If your age has no bearing of survivial, then the rates should be the same. 

Here are the counts of Adult / Children among the survivors only:


```python
survivors = passengers[passengers['Survived'] ==1]
survivors['AgeCat'].value_counts()
```

### 1.3 You Code

Create an `agecat_comparision_df` dataframe, similar to how we did for the `sex_comparision_df`.  

- Create a series of value counts for all passengers on "AgeCat"
- Create a 2nd series of value counte for only survivors on "AgeCat"
- Create a dataframe from the two series for comparison in a table
- Calculate survival rate of the "AgeCat" variable


```python
# todo write code here

```

**So, children had a 50% survival rate, better than the overall rate of 38%**

## So, women and children first?

It looks like the RMS really did have the motto: "Women and Children First."

Here are our insights. We know:

- If you were a passenger, you had a 38% chance of survival.
- If you were a female passenger, you had a 74% chance of survival.
- If you were a child passenger, you had a 50% chance of survival. 


### Now you try it for Passenger Class

Repeat this process for `Pclass` The passenger class variable. Make the same 3 column dataframe as you did in 1.3 only now use "Pclass" instead of "AgeCat"

I'll give you a hint... "Class matters!"

### 1.4 You Code


```python
# todo write code here

```

**Not a big surprise. The 1st class passengers had a 62.9% survival rate!**


## What have we learned?

Your best odds of survival were:

 - First class ticket: `Pclass==1`
 - Female: `Sex == Female`
 - Child: `AgeCat == Child`
 
Your job is to check the survival rate of those individuals, by engineering a file column, Let's call it `1stClassFemaleChild`  

Here's the process

    1. add a column to `passengers` called `1stClassFemaleChild`, and set the initial value to "No" for the entire dataset
    2. Set the first class passengers who are female children to "Yes". The code uses the dataframe "AND" operator and is provided for you:
    passengers['1stClassFemaleChild'][
        (passengers["Pclass"] == 1) &
        (passengers["AgeCat"] == "Child") &
        (passengers["Sex"] == "female")] = "Yes"
    3. get the value_counts() Series for the "1stClassFemaleChild" column. There should be 11 "Yes" values
    4. get the value_counts() Series for the "1stClassFemaleChild" column for suriviors only.  There should be 10 "Yes" values
    5. Build your 3-columns dataframe like you did in 1.3 and 1.4 consisting of "AllPassengers", "SurvivorsOnly" and "SurvivialRate"
 
    
**You will learn that while only 38% of all passengers survivied, 90.9% passengers meeting this criteria survivied! However the sample size n=11 is small.**

### 1.5 You Code


```python
# todo write code here


```
