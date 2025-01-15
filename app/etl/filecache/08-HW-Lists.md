# Homework: The Fudgemart Products Catalog

## The Problem

**Fudgemart**, a knockoff of a company with a similar name, has hired you to create a program to allow customers to browse their product catalog. 

Write an ipython interactive program that allows the user to select a product category from the drop-down and then displays all of the fudgemart products within that category. You can accomplish this any way you like and the only requirements are you must:

- load each product from the `fudgemart-products.txt` file into a list.
- build the  list of product catagories dynamically ( you cannot hard-code the categories in)
- print the product name and price for all products selected
- use ipython interact to create a drop-down for the user interface.


### File Format

 - the file `fudgemart-products.txt`  has one row per product
 - each row is delimited by a `|` character. This is called a "pipe"
 - there are three items in each row. category, product name, and price.
 - Example Row: `Hardware|Ball Peen Hammer|15.99`
   - Category = `Hardware`
   - Product = `Ball Peen Hammer`
   - Price = `15.99`


### Important Concepts From this homework

As you complete this program you will learn two important concepts in computing:

**Data Deduplication:** Taking a list of values as input and then outputting another list where the is only one unique value for each instance.   

For Example: `dedupe([1,1,2,3,5,5,6]) == [1,2,3,5,6]`


**Parallel Lists** Parallel lists are used to create tables of data by creating multiple lists. For the data table the lists share a common index.

For example:
    
    name age gpa
    Abby 40  3.6
    Bob  45  3.0
    Che  40  3.4
    
If we read the `Name` into one list and the `Age` into another, and `GPA` into yet another, then the first row of data is:

     name[0], age[0], gpa[0]
     
Likewise the last row is:

    name[-1], age[-1], gpa[-1]
    
Furthermore, any given row can be represented by a single `index` variable:

    # Print the table
    for index in range(len(name)):
        print(name[index], age[index], gpa[index])

## Approach:

This assignment is broken up into parts. We will use problem simplification to solve this problem.

- **You Code 2.1** Write a `dedupe()` function.
- **You Code 2.2** Write `load_fudgemart()` function to read in the data file and output the parallel lists. 
- **You Code 2.3** Write a text-only program to input a product category, then output the product info in that category.
- **You Code 2.4** Write an interact to complete the program: dropdown list of product categories, and upon selection display the products in that category.

Similar to the Small Group, we will take a **bottom up approach**. This means you should **hold off on completing part 1, until you are on step 2.3**


### Code to fetch data files

Run this code to download the data files required by this homework.


```python
! curl https://raw.githubusercontent.com/mafudge/datasets/master/ist256/08-Lists/test-fudgemart-products.txt -o test-fudgemart-products.txt
! curl https://raw.githubusercontent.com/mafudge/datasets/master/ist256/08-Lists/fudgemart-products.txt -o fudgemart-products.txt
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

### You Code 2.1: Write a `dedupe()` function.

In this first part, you will write the `dedupe()` function. An algorithm will be provided for you. It is your responsibility is to write the function and ensure it passes the tests provided. Once again. DO NOT edit the tests! If the test code doesn't work then your function is wrong. Debug your function until all tests pass!!!

Function doc string:
`dedupe(items: list ) -> list`

Input: list of items  
Output: list of items without duplicates  


Algorithm:

    start with an empty list called deduplicated
    for each item in the list of items
        if the item is NOT in the deduplicated list
            add the item to the deduplicated list
            
    after the for loop: sort the deduplicated data
    return back the sorted deduplicated data

Hints:

- Read the python docs on lists and list methods https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types 
- Here's a nice list tutorial: https://www.w3schools.com/python/python_lists.asp


```python
# SOLUTION CELL 2.1


```


```python
# Tests for 2.1
def test_dedupe(items: list, expected: list):
    actual = dedupe(items)
    print(f"dedupe: For items {items}, EXPECT={expected}, ACTUAL={actual}")
    assert all(e == a for e, a in zip(expected, actual))


test_dedupe([1, 1], [1])
test_dedupe(["A", "B", "B", "C", "C"], ["A", "B", "C"])
test_dedupe([1, 2, 1, 3, 2, 1, 2, 3, 3, 1, 2], [1, 2, 3])
```

### You Code 2.2: Write a `load_fudgemart()` function.

In this first part, you will write the `load_fudgemart()` function. once again an algorithm will be provided for you. It is your responsibility is to write the function and ensure it passes the tests provided. DO NOT edit the tests! If the test code doesn't work then your function is wrong. Debug your function until all tests pass!!!

Function doc string:
`load_fudgemart(filename: str ) -> tuple[list,list,list]`

Input: string name of file to load
Output: list of product_category, list of product_name, list of prodcut_price


Algorithm:

    create empty lists for categories, products, and prices
    open the file for reading
        for each line in the file
            strip the line then split the line on the pipe delimiter into 3 parts: cat, prod, price
            append the cat to the category list
            append the prod to the prod list
            append the price to the price list
            
    after the for loop: return the three lists back to the caller categories, products and prices
    


```python
# SOLUTION CELL 2.2

```


```python
# Tests for 2.1
def test_load_fudgemart(filename: str, index: int, expected_cat: str, expected_prod: str, expected_price: str):
    actual_categories, actual_products, actual_prices = load_fudgemart(filename)
    print(f'''
        load_fudgemart: For filename {filename}, index={index}
            EXPECT=({expected_cat},{expected_prod},{expected_price})
            ACTUAL=({actual_categories[index]},{actual_products[index]},{actual_prices[index]})
    ''')
    assert expected_cat == actual_categories[index] and \
        expected_prod == actual_products[index] and \
        expected_price == actual_prices[index]


test_load_fudgemart("test-fudgemart-products.txt",0,"hardware","hammer","14.97")
test_load_fudgemart("test-fudgemart-products.txt",1,"hardware","saw","9.97")
test_load_fudgemart("test-fudgemart-products.txt",2,"clothing","boots","22.99")

```

### You Code 2.3 Write final program

Now that we have the components `dedupe` and `load_fudgemart` its time to USE them to solve the original problem, assembing our components through a bottom-up appoach.

The program should:

    - Read in `fudgemart-products.txt` 
    - allow the user to input a category such as hardware or clothing.
    - if and only if the category entered is a valid category
    - display all products (category, name and price) matching the category.
    - Note: you will need to use the parallel list concept as explained at the top of the homework, specifically with respect to looping over the parallel arrays.
    

Before you Write 2.3, go back to **Part 1: Problem Analysis** and complete your INPUT, OUTPUT, and STEPS sections!


```python
# SOLUTION CELL 2.3
# Copy your dedupe() function here

# Copy your load_fudgemart() function here

# On with the MAIN PROGRAM

```

### You Code 2.4 Ipywidgets

Let's re-write the code as an `@interact_manual` You will need one input widget your list of deduplicated categories.    



```python
# SOLUTION CELL 2.4
from ipywidgets import interact_manual


```
