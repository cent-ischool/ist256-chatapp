# Class Coding Lab: Conditionals

The goals of this lab are to help you to understand:

- Relational and Logical Operators 
- Boolean Expressions
- The if statement
- Try / Except statement
- How to create a program from a complex idea.


# Understanding Conditionals

Conditional statements permit the non-linear execution of code. Take the following example, which detects whether the input integer is odd or even:


```python
number = int(input("Enter an integer: "))
if number %2==0:
    print(f"{number} is even")
else:
    print(f"{number} is odd")
```

NOTE: Make sure to run the cell more than once, inputting both odd and even integers to try it out. After all, we  don't know if the code really works until we test out both options!

On line 2, you see `number %2 == 0` this is a Boolean expression at the center of the logic of this program. The expression says **number when divided by 2 has a reminder (%) equal to (==) zero**. The key to deciphering this is knowing how the `%` and `==` operators work. Understanding the basics, such as these, areessential to problem solving with programming, for once you understand the basics programming becomes an exercise in assembling them together into a workable solution.

The `if` statement evaluates this Boolean expression and when the expression is `True`, Python executes all of the code indented underneath the `if`. In the event the Boolean expression is `False`, Python executes the code indented under the `else`. The code we indent is called a **block**.


### 1.1 You Code: Debugging

The code below is similar to the intial program. Instead of odd or even it uses a different Boolean expression to determine if the number is "Zero or Positive"or "Negative" otherwise.

Debug this code so that it works correctly. Here are some sample inputs to test and the expected outputs.

    Input: 10 Output: "Zero or Positive"
    Input: 0 Output: "Zero or Positive"
    Input: -10 Output: "Negative"
    


```python
# TODO Debug this program
number = int(input("Enter an integer: "))
if number>0:
     print("Zero or Positive")
else:
print("Negative")
```

# Rock, Paper Scissors

In this part of the lab we'll build out a game of Rock, Paper, Scissors. If you're not familiar with the game, I suggest reading this: [https://en.wikipedia.org/wiki/Rock%E2%80%93paper%E2%80%93scissor](https://en.wikipedia.org/wiki/Rock%E2%80%93paper%E2%80%93scissors) Knowledge of the game will help you understand the lab much better.

The objective of the lab is to teach you how to use conditionals but also get you thinking of how to solve problems with programming. We've said before its non-linear, with several attempts before you reach the final solution. You'll experience this first-hand in this lab as we figure things out one piece at a time and add them to our program.

## Here's our initial To-Do list, we've still got lots to figure out.

    1. computer opponent selects one of "rock", "paper" or "scissors" at random
    2. you input one of "rock", "paper" or "scissors"
    3. play the game and determine a winnner... (not sure how to do this yet.)


## Randomizing the Computer's Selection 
Let's start by coding the TO-DO list. First we need to make the computer select from "rock", "paper" or "scissors" at random.


To accomplish this, we need to use python's `random` library, which is documented here: [https://docs.python.org/3/library/random.html](https://docs.python.org/3/library/random.html) 
It would appear we need to use the `choice()` function, which takes a sequence of choices and returns one at random. Let's try it out.


```python
import random
choices = ['rock','paper','scissors']
computer = random.choice(choices)
print(computer)
```

Run the cell until you see all three choices appear at random. It make take more than 3 tries. It should make a random selection from `choices` each time you run it.

How did I figure this out? Well I started with a web search and then narrowed it down from the Python documentation. You're not there yet, but at some point in the course you will be. When you get there you will be able to teach yourself just about anything!

## Getting input for Your choice

With step one out of the way, its time to move on to step 2. Getting input from the user.


```python
# 1. computer opponent select one of "rock", "paper" or "scissors" at random
import random
choices = ['rock','paper','scissors']
computer = random.choice(choices)

# 2. you input one of "rock", "paper" or "scissors"
you = input("Enter your choice: rock, paper, or scissors: ")
print("You chose %s and the computer chose %s" % (you,computer))

```

# And guarding against stupidity


This is taking shape, but if you re-run the example and enter `pizza` you'll notice a problem. 

We should guard against the situation when someone enters something other than 'rock', 'paper' or 'scissors' This is where our first conditional comes in to play.

### In operator

The `in` operator returns a Boolean based on whether a value is in a list of values. Let's try it:



```python
# TODO run this:
print('rock' in choices, 'mike' in choices)
```

### 1.2 You Code

Now modify the code below to only print your and the computer's selections when your input is one of the valid choices. Replace `TODO` on line `8` with a correct Boolean expression to verify what you entered is one of the valid choices. Make sure to test your code with all three valid choices, plus a 4th invalid choice, like `pizza`. Use the `in` operator like in the example above.


```python
# 1. computer opponent select one of "rock", "paper" or "scissors" at random
import random
choices = ['rock','paper','scissors']
computer = random.choice(choices)

# 2. you input one of "rock", "paper" or "scissors"
you = input("Enter your choice: rock, paper, or scissors: ")
# replace "TODO" on this line with the correct Boolean expression
if (TODO):
    print(f"You chose {you} and the computer chose {computer}")
    # 3. play the game and determine a winnner... (not sure how to do this yet.)
else: 
    print("You didn't enter 'rock', 'paper' or 'scissors'!!!")
```

## Playing the game

With the inputs figured out, it's time to work on the final step, playing the game. The game itself has some simple rules:

- rock beats scissors (rock smashes scissors)
- scissors beats paper (scissors cut paper)
- paper beats rock (paper covers rock)

So for example:

- If you choose rock and the computer chooses paper, you lose because paper covers rock. 
- Likewise if you select rock and the computer choose scissors, you win because rock smashes scissors.
- If you both choose rock, it's a tie.

## It's too complicated!

It still might seem too complicated to program this game, so let's use a process called **problem simplification** where we solve an easier version of the problem, then as our understanding grows, we increase the complexity until we solve the entire problem.

One common way we simplify a problem is to **constrain our inputs**. If we force us to always choose `rock` (line 8), the program becomes a little easier to write.  Lines 13 to 18 were added - a single **if else** ladder to compare your input of `rock` against the computer's random selection of:

- `scissors` (you win: scissors cut paper)
- `paper` (you lose: paper covers rock)
- `rock` (tie) 

Run this code until you see all three outcomes based on the computer's choice.


```python
# 1. computer opponent select one of "rock", "paper" or "scissors" at random
import random
choices = ['rock','paper','scissors']
computer = random.choice(choices)

# 2. you input one of "rock", "paper" or "scissors"
# for now, make this 'rock'
you = 'rock' #input("Enter your choice: rock, paper, or scissors: ")
if (you in choices):  
    print("You chose %s and the computer chose %s" % (you,computer))
    
    # 3. play the game and determine a winnner (assuming rock only for user)
    if (you == 'rock' and computer == 'scissors'):
        print("You win! Rock smashes scissors.")
    elif (you == 'rock' and computer=='paper'):
        print("You lose! Paper covers rock.")
    else:
        print("It's a tie!")    
else: 
    print("You didn't enter 'rock', 'paper' or 'scissors'!!!")
```

Run the code in the cell above enough times to verify it works. (You win, you lose and you tie.) That will ensure the code you have works as intended.

## Paper: Making the program a bit more complex.

With the rock logic out of the way, its time to focus on paper. We will assume you always type `paper` and then add the conditional logic to our existing code handle it.

At this point you might be wondering should I make a separate `if` statement or should I chain the conditions off the current if with `elif` ?  Since this is part of the same input, it should be an extension of the existing `if` statement. You should **only** introduce an additional conditional if you're making a separate decision, for example asking the user if they want to play again. Since this is part of the same decision (did you enter 'rock', 'paper' or 'scissors' it should be in the same `if...elif` ladder.


### 1.3 You Code

In the code below, I've added the logic to address your input of 'paper' You only have to replace the `TODO` in the `print()` statements with the appropriate message. 


```python
# 1. computer opponent select one of "rock", "paper" or "scissors" at random
import random
choices = ['rock','paper','scissors']
computer = random.choice(choices)

# 2. you input one of "rock", "paper" or "scissors"
# for now, make this 'rock'
you = 'paper' #input("Enter your choice: rock, paper, or scissors: ")
if (you in choices):  
    print("You chose %s and the computer chose %s" % (you,computer))

    # 3. play the game and determine a winnner (assuming paper only for user)
    if (you == 'rock' and computer == 'scissors'):
        print("You win! Rock smashes scissors.")
    elif (you == 'rock' and computer=='paper'):
        print("You lose! Paper covers rock.")
    elif (you == 'paper' and computer =='rock')
        print("TODO - What should this say?")
    elif (you == 'paper' and computer == 'scissors')
        print("TODO - What should this say?")
    else:
        print("It's a tie!")    
else: 
    print("You didn't enter 'rock', 'paper' or 'scissors'!!!")
```

## The final Rock, Paper, Scissors program

With the `rock` and `paper` cases out of the way, we only need to add `scissors` logic. We leave this part to you as your final exercise. 

### 1.4 You Code

Similar to the `paper` example you will need to add two `elif` statements to handle winning and losing when you select `scissors` and should also include the appropriate output messages.



```python
import random
choices = ['rock','paper','scissors']
computer = random.choice(choices)
you = input("Enter your choice: rock, paper, or scissors: ")
if (you in choices):  
    print("You chose %s and the computer chose %s" % (you,computer))
    if (you == 'rock' and computer == 'scissors'):
        print("You win! Rock smashes scissors.")
    elif (you == 'rock' and computer=='paper'):
        print("You lose! Paper covers rock.")
    elif (you == 'paper' and computer =='rock'):
        print("You win! Paper beats rock.")
    elif (you == 'paper' and computer == 'scissors'):
        print("You lose! Scissors beat paper.")
    # TODO: add code here
    else:
        print("It's a tie!")    
else: 
    print("You didn't enter 'rock', 'paper' or 'scissors'!!!")
```

# Exceptions 

Exceptions are a special type of conditional. They do not branch based on a Boolean expression. Instead they branch whenever an error occurs. We use the `try...except` statement to handle error gracefully when our code runs.

Here's a classic example of code that could use some error handling. Enter a GPA of `awesome`


```python
gpa = float(input("Enter your GPA:" ))
pts_away = 4.0 - gpa
print(f"You are {pts_away} from a 4.0")
```

Because the input is not convertable to type `float` this causes a `ValueError` and the demise of our program. It stops working and crashes rather ungracefully.

It's not ideal to send these types of error messages to the users of our programs. so we can use `try..except` to handle the error more gracefully.


```python
try: #Check for errors
    gpa = float(input("Enter your GPA:" ))
    pts_away = 4.0 - gpa
    print(f"You are {pts_away} from a 4.0")
except ValueError: # if its a ValueError, do this...
    print("Error: That is not a valid value for a GPA")
```

## Simple Rules for Handling Errors

- We should not worry about handling errors until our program works with the expected inputs.
- This approach should only be used to handle errors. Not for making decisions.
- "Exceptions are exceptional:" They should be used when there is no alternative to solving the problem. 


## On Your Own

Use What you've learned about `if` and `try` except. To write a program that when you input any number, and will output whether or not the number is positive. 

Example runs:

    Input: 10.5 Output: Positive
    Input: 0    Output: Not Positive
    Input: -5.1 Output: Not Positive
    Input: abc  Output: Not a Number


Algorithm:


    Try this code:
        input a float
        if input number greater than zero
            print "Positive"
        else
            print "Not positive"
    if there's an error
        print "Not a Number"
        

### 1.5 You Code


Convert the algorithm into code here:



```python
# TODO Write Code here
```
