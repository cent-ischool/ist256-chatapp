# Homework: People Enslaved on Plantations in St. Lucia, 1815.

Dr. Murphy from the Maxwell school and I collaborated on a research project to build a searchable database of enslaved individuals from St. Lucia. The data came from a British census of the Caribbean island in 1815. Great Britain had recently secured the island in 1814 from the French following the Treaty of Paris ending the Napoleonic Wars. 

This project posed unique challenges as the census data were scanned pages of hand-written census data in French. The unique nature of the data made it difficult to automate so we used student volunteers to read the page and translate then transcribe the data into a spreadsheet, so we could then build the dataset. Here is an example of one of these pages:

[https://imgur.com/a/usMqX1c](https://imgur.com/a/usMqX1c)

The impact of the project was significant. Before our work there was no searchable registry of individuals from this census. Our dataset, to be published to the Journal of Slavery and Data Preservation,  https://jsdp.enslaved.org, will be searchable by name as well as other characteristics. We are hoping people will use the dataset to help learn about the history of St. Lucia and make connections in their genealogical histories. 

Dr. Murphy and I appeared on the 'Cuse Conversations podcast in 2023. If you're intereted in our work, give it a listen.

https://podcasters.spotify.com/pod/show/cuseconversations/episodes/Reconstructing-the-Lives-and-Genealogies-of-Enslaved-People-Maxwell--iSchool-Faculty-Partner-on-Searchable-Database-e2187me/a-a9in78h

## The Assignment

For this assignment, you will use an abridged version of this dataset. It consists of two parts:

- `https://raw.githubusercontent.com/mafudge/datasets/master/st-lucia/St-Lucia-1815-Plantation-Only.csv` This dataset contains a list of plantations from the registry. One row is a plantation. The plantation a summary of the number of people enslaved on the plantation, but does not include any details as to who they individuals are.
- `https://raw.githubusercontent.com/mafudge/datasets/master/st-lucia/parishes.csv` geocoded districts of St. Lucia in 1815  which you can use to display a map.

The goal for this assignment is to practice data exploration and then build a data product. 

- **You Code 2.1** Data Exploration. You will complete a series of code challenges similar to the lab and smallgroup. Unlike your project, you will be given questions to answer, and need to write Python code to answer them.
- **You Code 2.2** Data Product. You will build a data story based on your data exploration. Again this will be a guided process.  You will hold off on completing the problem analysis until this section.


## Part 1: Problem Analysis

You will complete a problem analysis for the data product to tell a story in 2.2. **Since we are using data exploration in 2.1, do not attempt this step until step 2.2**


### 1.1 Program Outputs

Describe your program outputs in the cell below. 




### 1.2 Program Inputs

List out the program inputs in the cell below.




### 1.3 The Plan (Algorithm)

Explain, as specifically as you can, without writing code, how the program works from input to output. Be detailed with your plan as you will need to turn it into code. 




## Part 2: Code Solution

You may write your code in several cells, but place the complete, final working copy of your code solution within this single cell below. Only the within this cell will be considered your solution. Any imports or user-defined functions should be copied into this cell. 


```python
import pandas as pd
import seaborn as sns
import folium
from IPython.display import display
from ipywidgets import interact_manual
```


```python
plantation_url = "https://raw.githubusercontent.com/mafudge/datasets/master/st-lucia/St-Lucia-1815-Plantation-Only.csv"
parishes_url = "https://raw.githubusercontent.com/mafudge/datasets/master/st-lucia/parishes.csv"

# Load the datasets, We need to use a special text encoding for the accents.
plantations = pd.read_csv(plantation_url, encoding="ISO-8859-1")
parishes = pd.read_csv(parishes_url, encoding="ISO-8859-1")

# Combine the datasets together on Parish so that we have GPS coordinates for them
df = pd.merge(left=plantations, right=parishes, how="inner", left_on="Location (Parish)", right_on="Parish")

# Add a count column to make our visualizations easier to produce, similar to labs and small group
df['count'] = 1

# take a peek at the columns
df.sample()
```

### You Code 2.1: Data Explorations

Before we build a data story, we must figure out which story we want to tell. This is generally accomplished by exploring and visualizing the dataset.

    2.1.a. Data Set Information: Number of plantations in dataset? Number of columns?
    2.1.b  Number of enslaved peoples in dataset?
    2.1.c  Plot the count of plantations by district/parish
    2.1.d  Plot the count of plantations by plantation owner's sex
    2.1.e  Plot of total number of enslaved peoples by location/parish
    2.1.f  Filter out plantations with unknown main production (?)
    2.1.g  Plot of counts of plantations by production, excluding the unknowns. `Coffee`, `Sugar`, etc...

For each of the following, output using the `display()` function, or directly to the cell output. **Make sure your bar charts are legible.** Proceed to swap the x/y axis if necessary.

**There are not automated code checks for 2.1. Your work will be graded manually.**


```python
# SOLUTION CELL 2.1.a. Data Set Information: Number of plantations in dataset? Number of columns?

```


```python
# SOLUTION CELL 2.1.b  Number of enslaved peoples in dataset?

```


```python
# SOLUTION CELL 2.1.c  Plot the count of plantations by district/parish

```


```python
# SOLUTION CELL 2.1.d  Plot the count of plantations by plantation owner's sex

```


```python
# SOLUTION CELL 2.1.e  Plot of total number of enslaved peoples by location/parish

```


```python
# SOLUTION CELL 2.1.f  Filter out plantations with unknown main production (?)

```


```python
# SOLUTION CELL 2.1.g  Plot of counts of plantations by production, excluding the unknowns. `Coffee`, `Sugar`, etc...

```

### You Code 2.2: Data Product

The last Plot is interesting. Let's use it in our data story. We want to help the user of our program undersand which goods were produced on St. Lucia plantations and the where on the island they were produced. 

The user types in a production such as `Coffee`, `Sugar`, `Cassava`, `Cacao`, etc...

Then the appliction displays:

- A chart counting the number of plantations in each parsh that produces the product
- A map of St. Lucia with a pin in each parish that produces the products. The marker popup should show the parish name

Details of the process:

- filter out the ? from the Main production
- filter out the columns to only what you need: `Main Production`, `Parish`, `count`, `Lat`, `Lon`
- based on the input, use `find()` to filtered the input production value. We did something similar in a previous assignment, lab or small group.
- with the filtered dataframe display counts of plantations by parish
- with the filtered dataframe display the pins on a map


Here's a video of the final data product in action:

[https:////imgur.com/a/4N2C9ad](https://imgur.com/a/4N2C9ad)



**There are not automated code checks for 2.2. Your work will be graded manually.**



```python
# SOLUTION CELL 2.2
import pandas as pd
import seaborn as sns
import folium


```
