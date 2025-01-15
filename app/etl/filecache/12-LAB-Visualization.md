# In-Class Coding Lab: Data Visualization

The goals of this lab are to help you understand:

 - The value of visualization: A picture is worth 1,000 words!
 - The various ways to visualize information
 - The basic requirements for any visualization
 - How to plot complex visualizations such as multi-series charts and maps
 - Visualization Tools:
     - Matplolib
     - Plot.ly
     - Folium Maps
     


```python
import pandas as pd
import seaborn as sns
import folium

import warnings
from IPython.display import display
from ipywidgets import interact_manual
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

%matplotlib inline
```

## The movie goers data set

For this lab, we will use the movie goers data set. This data set is a survey demographic survey of people who go to the movies. Let's reload the data and setup our `age_group` feature of `Youth`, `Adult` and `Senior`. We will also create a measure column, `count` because this dataset has no definitive measures such as the price someone paid to see the movie.


```python
goers = pd.read_csv('https://raw.githubusercontent.com/mafudge/datasets/master/ist256/13-visualization/moviegoers.csv')
goers['age_group'] = ''
goers['age_group'][goers['age'] <=18] = 'Youth'
goers['age_group'][(goers['age'] >=19) & (goers['age'] <=55)] = 'Adult'
goers['age_group'][goers['age'] >=56] = 'Senior'
goers['count'] = 1
goers.sample(5)
```

## Visualizing Data

There are many ways your can visualize information. Which one is the most appropriate? It depends on the data, of course. 

- **Counting Categorial data** belongs in *charts like bar charts*.
- **Counting Numerical data** is best suited for *histograms*.
- **Timeseries data and continuous data** belongs in *line charts*.
- **A comparision of two continuous values** is best suited for a *scatter plot*. 
- **Geographical data** is best displauyed on *maps*.

Let's use this knowledge to plot some data in the `goers` `DataFrame`!

## Males or Females?

The first thing we might want to visualize is a count of gender in the dataset. A `barplot()` is well suited for this task as it displays data as a portion of a whole. 

To create a bar chart we place the category, `gender` on the x-axis, the value to count `count` on the y-axis, and we set the `estimator='sum'` since we want to add up the values.



```python
sns.barplot(data=goers, x="gender", y="count", estimator="sum")
```

Genders are out of balance!

Here's the same information without the plot:


```python
goers['gender'].value_counts()
```

### 1.1 You Code

Create a bar chart for the `age_group` series. We want to `sum` up the `count`. like we did in the previous example. Which group has the most movie goers?



```python
#todo write code here

```

## Looking at occupations

Check out this plot of occupations. Very busy


```python
sns.barplot(data=goers, x="occupation", y="count", estimator="sum")
```

**The solution is to swap the X and Y.**

This rotates the plot on its side which is easier to read! Common for bar charts with long label names and many categories.

Also we add a splash of color with the `hue=` argument.


```python
sns.barplot(data=goers, y="occupation", x="count", estimator="sum", hue="occupation")
```

Ahh. that's much better. So much easier to understand! 

Lots of students going to the movies. Looks like I need to assign more homework!

### 1.2 You Code

create a `barplot()` similar to the example above but break the occupations up by gender.Each gender should be listed next to the occupation. Are they female doctors in the dataset?


```python
# todo write code here

```

## Origin of the Histogram

Bar charts are not suitable for continuous values. For example, let's create a bar chart for ages: 


```python
sns.barplot(data=goers, x="age", y="count", estimator="sum", hue="age")
```

Not helpful. Why?

1. too many categories. Theres a bar for each age
2. age is a continuous variable not a categorical variable. In plain English, this means there's a relationship between one age and the next.  20 < 21 < 22. This relationship is not represented in a bar chart, which only displays categories of data.

## ...Call in the Histogram!

What we want is a **historgram**, which takes a continuous variable and loads counts into "bins". Let's try it:


```python
sns.histplot(data=goers, x="age")
```

The `histplot()` peforms automatic binning. Let's add a second dimension to the hisogram to overay `Gender`. From the output you can see how there are many more Male movie goers in all the age groups.


```python
sns.histplot(data=goers, x="age", hue="gender")
```

### 1.3 You Code

Write a one-liner to make a histogram of Movie goeer ages by age group. At first glance this might seem like a silly thing to do but the visual is actually quite interresting, and you can clearly see which part of the data distributions are `Adult`, `Senior` and `Youth`.


```python
# todo write code here

```

## Interactive Data Products

After exploring your data, you might decide on a compelling data product. For example:

I'd like to allow a user to compare age distributions (like in 1.3) but for two occupations. So for example the user selects `student` and `scientist` and then it outputs two `histplots()` similar to 1.3 but filtered to only those selections. Let's build that now.

### Dedupe the occupation

this code dedupes the occupation


```python
occupations = sorted(list(goers['occupation'].dropna().unique()))
occupations
```

### Build the input widgets


Next let's build the input widgets. This code sample creates the input widgets from the `occupations` list. It then filters each occupation and displays two random rows `sample()` from each filtered dataframe.


```python
occupations = sorted(list(goers['occupation'].dropna().unique()))
@interact_manual(occupation1=occupations, occupation2=occupations)
def onclick(occupation1, occupation2):
    occdf1 = goers[goers['occupation']==occupation1]
    occdf2 = goers[goers['occupation']==occupation2]
    display(occdf1.sample(2))
    display(occdf2.sample(2))

```

### 1.4 You Code

Write the complete program. Most of the code has been written for you. All you need to do is put in the proper `data=` `x=` and `hue=` arguments for the two hist plots. 



```python
# todo: write code here
occupations = sorted(list(goers['occupation'].dropna().unique()))
@interact_manual(occupation1=occupations, occupation2=occupations)
def onclick(occupation1, occupation2):
    occdf1 = goers[goers['occupation']==occupation1]
    occdf2 = goers[goers['occupation']==occupation2]
    fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=False)
    sns.histplot(data=??, x=??, hue=??, ax=ax1)
    sns.histplot(data=??, x=??, hue=??, ax=ax2)
    ax1.title.set_text(occupation1)
    ax2.title.set_text(occupation2)


```

## Folium for Mapping

Folium is a Python module wrapper for [Leaflet.js](http://leafletjs.com/), which uses [Open Street Maps](https://www.openstreetmap.us/). These are two, popular open source mapping libraries. Unlike Google maps API, its 100% free!

You can use Folium to render maps in Python and put data on the maps. Here's how easy it is to bring up a map:



```python
CENTER_US = (39.8333333,-98.585522)
movie_map = folium.Map(location=CENTER_US, zoom_start=4)
display(movie_map)
```

You can zoom right down to the street level and get amazing detail. T

### Mapping the "executive" movie goers.

Let's take one category of movie goers and map their whereabouts. We will first need to import a data set to give us a lat/lng for the `zip_code` we have in the dataframe. We could look this up with Google's geolookup API, but that's too slow as we will be making 100's of requests. It's better to have them stored already and merge them with `goers`!

Let's import the zipcode database into a Pandas DataFrame, then merge it with the `goers` DataFrame:


```python
zipcodes = pd.read_csv('https://raw.githubusercontent.com/mafudge/datasets/master/zipcodes/free-zipcode-database-Primary.csv', dtype = {'Zipcode' :object})
data = goers.merge(zipcodes,  how ='inner', left_on='zip_code', right_on='Zipcode')
execs = data[ data['occupation'] == 'executive']
execs.sample(3)
```

### 1.5 You Code: Mapping Executives

Similar to WMC2 and the assigned reading from thsi week, loop over the `execs` dataframe  and add them to the map as a marker. The algorithm


    for each row in execs dataframe
        dd = the row's Lat/Long
        text = a string of the row's  age, gender, occupation, city and state
        make a marker at location dd with popup text
        add the marker to movie_map
        
    display movie_map


```python
## todo write code here!

```
