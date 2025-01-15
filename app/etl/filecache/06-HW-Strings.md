# Homework: Understanding Sentiment Analysis

**DO NOT FORGET!** The purpose of the homework is to reinforce concepts from the unit through practice and help you to become a better programmer and computational thinker. There are dozens of methods for performing sentiment analysis and all of them are better than this one... but then again this assignment really isn't about sentiment analysis! ;-)

## The Problem

Sentiment Analysis is a natural language processing technique used to determine the mood of text, classified as positive, negative or neutral.  It has practical applications for analyzing reactions in social media, customer relationship managment,  comments / reviews, feedback and much more. For more information, see: [https://monkeylearn.com/blog/sentiment-analysis-examples/](https://monkeylearn.com/blog/sentiment-analysis-examples/)

In this homework assignment we will create a very basic sentiment analyzer that scores each word of the input text as positive `+1`, neutral `0`, or negative `-1`. The sum of all the words in the text becomes the sentiment score. Text with an overall score `>0` will be considered positive, likewise text will an overall score of `<0` will be considered negative. 


It's up to you to create the initial list of words you consider positive or negative. You will not need many to test your program. For inspiration of words you can use, consult:

- Positive words:  
[https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/blob/master/data/opinion-lexicon-English/positive-words.txt](https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/blob/master/data/opinion-lexicon-English/positive-words.txt) (Hu 2004)
- Negative words:  
[https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/blob/master/data/opinion-lexicon-English/negative-words.txt](https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/blob/master/data/opinion-lexicon-English/negative-words.txt) (Hu 2004)

### Example Runs

    Example Run #1

    Input Positive Words: happy joy fun
    Input Negative Words: angry sad mad
    Input Text to Analyze: Carlos was a happy lad.
    Sentiment Score: 1
   

    Example Run #2

    Input Positive Words: happy joy fun
    Input Negative Words: angry sad mad
    Input Text to Analyze: The mad lad was a sad dad. No fun!
    Sentiment Score: -1


## Approach

We will complete this program in several phases, using the problem simplification approach similar the last to homework assignemnts. 

- **You Code 2.1** Write a function, `score_sentiment()` which given 3 inputs: positive words, negative words and some text, will return an integer score of sentiment as output. Assume all inputs are lower case and do not have any punctuations. You will write this function blind - meaning you will not know whether it is actually working until You Code 2.2
- **You Code 2.2** Write a function `test_score_sentiment()` similar to the other test functions we have written and used in this course so far.  The function should take inputs for `score_sentiment()` along with an `expected` value, it should compute the `actual` value by calling `score_sentiment()` and then print the values, and `assert expected == actual`  
Write at least 3 tests for this function to produce an expected score of +2, -2 and 0 respectively.
-  **You Code 2.3** Write the main program using `input()` and `print()` functions. In this step you will copy in your `clean()` function from Small Group handle punctuation and lower-cased letters.
- **You Code 2.4** Re-write the main program to use `IPWidgets` and the `@interact_manual` decorator to auto-create the input widgets. 

### Citations 
++ Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews."   
Proceedings of the ACM SIGKDD International Conference on Knowledge   
Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle,   
Washington, USA,  

## Part 1: Problem Analysis

You will complete a problem analysis for the `score_sentiment()` function and the main program. 

Just remember the following:
  - The `score_sentiment()` function assumes the inputs were cleaned already.
  - The main program must `clean()` inputs before calling `score_sentiment()`
  - you should write a detailed algorithm for `score_sentiment()` but in the main program, it should just be a step because you plan to call the function

### 1.1 Program Outputs

Describe your program outputs in the cell below. 


    outputs for score_sentiment() function
    
    outputs for main program
    

### 1.2 Program Inputs

List out the program inputs in the cell below.


    inputs for score_sentiment() function
    
    inputs for main program

### 1.3 The Plan (Algorithm)

Explain, as specifically as you can, without writing code, how the program works from input to output. Be detailed with your plan as you will need to turn it into code. 


    steps for score_sentiment function
    
    steps for main program
    

## Part 2: Code Solution

You may write your code in several cells, but place the complete, final working copy of your code solution within  each cell labeled `# SOLUTION CELL` everything required to make the code work should be in this cell, as this is the cell that will get evaluated. 

### You Code 2.1 

Write a function, `score_sentiment()` which given 3 inputs: positive words, negative words and some text, will return an integer score of sentiment as output. Assume all inputs are lower case and do not have any punctuations. You will write this function blind - meaning you will not know whether it is actually working until You Code 2.2



```python
# SOLUTION CELL 2.1
def score_sentiment(TODO):
    return TODO

```

### You Code 2.2

Write a function `test_score_sentiment()` similar to the other test functions we have written and used in this course so far.  The function should take inputs for `score_sentiment()` along with an `expected` value, it should compute the `actual` value by calling `score_sentiment()` and then print the values, and `assert expected == actual`  
Write at least 3 tests for this function to produce an expected score of +2, -2 and 0 respectively.



```python
# SOLUTION CELL 2.2
def test_score_sentiment(pos: str, neg: str, text:str , expected: int) -> int:
    actual = score_sentiment(pos, neg, text)
    print(f"For POS={pos}, NEG={neg}, TEXT={text} EXPECT={expected}, ACTUAL={actual}")
    assert expected == actual


# ACTUAL TESTS HERE
# call test_score_sentiment and write your 3 tests


```

### You Code 2.3

Write the main program using `input()` and `print()` functions. In this step you will copy in your `cleanup()` function from Small Group handle punctuation and lower-cased letters.

This will be auto-checked based on the Example inputs at the top.



```python
# SOLUTION CELL 2.3

# PASTE IN YOUR def cleanup... FUNCTION FROM SMALL GROUP


# PASTE IN YOUR  def score_sentiment.. FUNCTION FROM ABOVE

# On with the MAIN PROGRAM
# INPUTS (nothing but input() statements here)

# PROCESS (clean and score the sentiment)

# OUTPUTS (nothing but print() statements here)

```

### You Code 2.4 

Re-write the main program to use `IPWidgets` and the `@interact_manual` decorator to auto-create the input widgets. IF you need to consult previous examples for assistance!

This solution will be checked manually by your instructor


```python
# SOLUTION CELL 2.4
from IPython.display import display, HTML
from ipywidgets import interact_manual, widgets

display(HTML("<H1>Sentiment Analysis</h1>"))
@interact_manual(text=widgets.Textarea(),pos="", neg="")
def onclick(TODO-REPLACE-WITH-INPUTS):
    # Process here

    # output Here

```
