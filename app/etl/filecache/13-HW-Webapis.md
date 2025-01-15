# Homework: Twitter Sentiment of Airlines


## The Problem

You work for a marketing firm and have been tasked with producing a data visualization of what people are saying on Twitter/X about each of the airlines you represent. Your firm represents 4 airlines: Gamma Airlines, JetBrown, Murcia Airways, and Untied Airlines.

A data engineer has extracted the "tweets" (as you might have guessed by now... its 100% made up) from the X API. You can find the tweets in `airline_tweets.csv`, along with who tweeted it and which airline they tweeted about in the file.

You will need to perform a **sentiment analysis** on each tweet to determine if the message is `positive`, `neutral` or `negative`.

The final product should allow the user to select an airline from a drop-down (or choose `*ANY*`) and then a bar chart of user / sentiment counts. Here's a screenshot with all airlines included.

#### Screenshot of Program

![https://i.imgur.com/LdouZjo.png](https://i.imgur.com/LdouZjo.png)


## The Assignment

Most of this code has been written for you. The `extract_sentiment()` and `dedupe_series()` functions are included here. They were written in previous assignments.  

What you need to figure out:

- **You Code 2.1** Data Preparation. Use `pd.apply()` to create a new series `df['sentiment']` which represents the sentiment of each tweet. Generate a `df['count']` column. Then write the dataframe to the file `airline_tweets_sentiment.csv` **This is important** if you keep calling the API, you will run out of credits, so once you figure out the sentiment, **never do it again!**. This is common practice in web API consumption and you should be adopting it for your project.

- **You Code 2.2** Data Product. Put it all together to read from ``airline_tweets_sentiment.csv`, build a dropdown of airlines, and then create the interact and barchart. The problem analysis should be for this part.


**IMPORTANT: The solution to this assignment consists of a whopping 12 lines of code.** Its more about putting the pieces together at this point than anything else.


## Part 1: Problem Analysis

You will complete a problem analysis for the data product to tell a story in 2.2. **Since we are using data preparation in 2.1, do not attempt this step until step 2.2**


### 1.1 Program Outputs

Describe your program outputs in the cell below. 




### 1.2 Program Inputs

List out the program inputs in the cell below.




### 1.3 The Plan (Algorithm)

Explain, as specifically as you can, without writing code, how the program works from input to output. Be detailed with your plan as you will need to turn it into code. 




## Part 2: Code Solution

You may write your code in several cells, but place the complete, final working copy of your code solution within this single cell below. Only the within this cell will be considered your solution. Any imports or user-defined functions should be copied into this cell. 


```python
import requests
import pandas as pd
import seaborn as sns
from IPython.display import display, HTML
from ipywidgets import interact_manual

# Place your CENT IoT API Key here
APIKEY = 'ea044c96950db6cc0fab7ae1'

def extract_sentiment(text: str) -> tuple[str, str]:
    text_input = {"text": text}
    url = 'https://cent.ischool-iot.net/api/azure/sentiment'
    headers = {'X-API-KEY': APIKEY}
    response = requests.post(url, headers=headers, data=text_input)
    response.raise_for_status()
    data = response.json()
    sentiment = data['results']['documents'][0]['sentiment']
    return sentiment

def dedupe_series(series: pd.Series, addany=True) -> list[str]:
    items = sorted(list(series.dropna().unique()))
    if addany:
        items.insert(0, "*ANY*")
    return items
```

### You Code 2.1: Data Preparation

Before we build the data story, we must prepare the dataset, there are 4 lines of code here:

    1) read in `airline_tweets.csv` into a dataframe
    2) Add a 'Count' Series/column to the dataframe, similar to the examples we did in the Visualization unit.
    3) Use `pd.apply()` to call the `extract_sentiment()` function for each tweet in the dataset, making a new Seriesn/column `Sentiment`.
    4) Save your work so you never have to do this again. Save as a csv file `"airline_tweets_sentiment.csv"`

**If you completed this part successfully the loaded `"airline_tweets_sentiment.csv"` will look like this:**

![https://i.imgur.com/rXQlfXS.png](https://i.imgur.com/rXQlfXS.png)

**NOTE: There is no automated code check for this part**


```python
# SOLUTION CELL 2.1 Prepare the data set

```

### You Code 2.2: Data Product

In this part you will load in your prepared file: `airline_tweets_sentiment.csv`, and build `list` from the `Airline` series for the interact.

The interact follows the same pattern we used in the UFO assignment: when the selected airline is not `*ANY*`, filter by the selection. Rather than showing data we output a bar chart of User / Sentiment counts.

Make sure to complete the problem analysis.

**NOTE: If you do this correctly, its 8 lines of code.**

**There are not automated code checks for 2.2. Your work will be graded manually.**



```python
# SOLUTION CELL 2.2



```
