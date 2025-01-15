# In-Class Coding Lab: Transformations with Pandas

This lab will explore some **Stocks** data as retrieved from **Yahoo Finance** in March of 2024. All of the data you will nee can be found in the `stocks` folder where you found this lab.

The emphasis of this lab is not data analysis per-se but instad how to deal with complex data sets, specifically:

 - reading data in JSON format
 - scraping HTML table data from the web
 - combining data sets using `concat()`
 - connecting data sets on a common column using `merge()`
 - custom operations using `apply()`



```python
import pandas as pd
import numpy as np
import json
from IPython.display import display
# this turns off warning messages
import warnings
warnings.filterwarnings('ignore')
```

## Reading in JSON data

The preferred method of reading in JSON data into a Pandas DataFrame is to deserialize the data with the `json` library and then use `pd.json_normalize()` to further process the data. As we saw in the reading for this week `json_normalize()` is quite powerful for handling the JSON format and has many options.  

If you observe the `stocks/company-info.json` file, you will see the JSON is *nested*. For example the `city` key is under the `info` key.

```
[
    {
        "symbol": "X",
        "name": "United States Steel Corporation",
        "exchange": "NYQ",
        "industry": "Steel",
        "sector": "Basic Materials",
        "info": {
            "website": "https://www.ussteel.com",
            "city": "PA",
            "state": "Pittsburgh",
            "country": "United States"
        }
    },
    ...
```

`json_normalize()` can handle nested JSON easily. 

### Why is nested JSON a problem?

run this code to read in the `company-info`:


```python
companies = pd.read_json("stocks/company-info.json")
companies[['info']].head()
```


```python
companies.info()
```

See the problem here? the `info` key in the JSON has 4 key-values. These are not accessible as the `read_json()` function does not inspect inside the keys for other nested JSON.

This means the values `website`, `city`, `state` and `country` are not accessible. :-(

### json_normalize() to the rescue!

By default `json_normalize()` will flatten the schema. It takes some extra work because you can't use it from a file.



```python
with open("stocks/company-info.json", "r") as f:
    data = json.load(f)

companies = pd.json_normalize(data)
companies.head()
```


```python
companies.info()
```

### 1.1 You Code

To demonstrate the nested values are available, use pandas filters to display these columns:

    - symbol
    - name
    - info.state
    
for only those companies in California `'CA'` as the boolean index.

Place the results in a separate dataframe variable and then display it.


```python
# todo write code here

```

## Simple web scraping with Pandas

The pandas `read_html(url)` method function allows us to read all the HTML tables on the webpage at the provided `url`. This is a quick a easy method of *web scraping* (parsing content from the web).

`read_html()` will return a list of every HTML table on the page. It's then up to us to figure out which one in the list is the one we want. 


### Example:

For example, visit this page in your web browser: [https://en.wikipedia.org/wiki/Display_resolution](https://en.wikipedia.org/wiki/Display_resolution)

About 1/2 down the page, there is a section titled **Common Display Resolutions** and within this section there is a data table. Let's capture this table in Pandas using code.

This code will read every table on the webpage, making a Python `list`:



```python
tables = pd.read_html("https://en.wikipedia.org/wiki/Display_resolution")
```

Let's iterate over the tables printing the index and the table itself. This makes it easier to find the table we want from the webpage. To get the index while we loop, we use the `enumerate()` function which returns the item and its index.


```python
for index, table in enumerate(tables):
    print("INDEX:", index)
    print("TABLE:")
    display(table.head(5))
```

### 18 tables?!?!?

That's a lot of tables, but it looks like the table at `index == 4` is the one we want!



```python
resolutions = tables[4]
display(resolutions.head(n=10))
```

Now that we have "discovered" where the table we want it located, we can tidy our code up as:


```python
tables = pd.read_html("https://en.wikipedia.org/wiki/Display_resolution")
# we we discovered its at index 4
resolutions = tables[4] 
display(resolutions.head(n=10))
```

### 1.2 You Code 

Write code to extract the **S&P 500 component stocks** table from this webpage:   

`https://en.wikipedia.org/wiki/List_of_S%26P_500_companies` [https://en.wikipedia.org/wiki/List_of_S%26P_500_companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)

TIP: Use the cell above this one to "figure it out" and once you know the exact code, place it in the cell below. Name the DataFrame variable `sandp`, and use the `display()` function to show a random `sample()` of 10 companies.


```python
# todo write code here

```

## Merging two DataFrames together on a common/maching column.

Right now we have 2 DataFrame sets of data

`companies` - our list of companies.  
`sandp` - the companies on the S&P 500 index


```python
companies.sort_values("symbol").head(5)
```


```python
sandp.sort_values("Symbol").head(5)
```

You can see that `AAPL` is on both our company list and the S&P500 company list.  Its great to observe that but even better to output it programmatically with code. 

### Join types

For two datasets, in this case:

```
+===========+                 +===========+
| companies |                 |   sandp   |
+===========+                 +===========+
|   Our     |                 |  S and P  |
| Companies |                 | 500 Index |
+-----------+                 +-----------+
| column:   |                 | column:   | 
|   symbol  |                 |  Symbol   | 
+-----------+                 +-----------+
```
Consider `companies` on the left and `sandp` on the right. Left and right are relative but we need some kind of positioning for reference.

Here are the 3 join possibilities `left`, `inner` and `right` along with their results.

```
+===========+  +===========+  +===========+
| how:left  |  | how:inner |  | how:right |
+===========+  +===========+  +===========+
| RESULTS:  |  | RESULTS:  |  | RESULTS:  |
| inner +   |  | only rows |  | inner +   |
| all rows  |  | IN BOTH   |  | all rows  |
|  from     |  | companies |  |  from     |
| companies |  | AND sandp |  | sandp     |
+-----------+  +-----------+  +-----------+

```

So in Summary

- `how='inner'` ==> the resulting DataFrame contains only matches from the `left` and `right`
- `how='left'` ==> the resulting DataFrame contains all of the `left` + matches from the `left` and `right`
- `how='right'` ==> the resulting DataFrame contains all of the `right` + matches from the `left` and `right`

### Which companies are not on the S&P 500?

Together let's figure out which `companies` are NOT on the `sandp`.

This is a two step process:

1. `merge()` the dataframes together using a `how='left'`. Because we said `left`, the results will include matches `companies['symbol'] == sandp['Symbol']` in addition to all the rows from `companies` (because its on the left).
2. Filter out any rows where the `joined['Symbol'].isna()` because if its `np.nan` that means there was no match.

And what remains are companies that are NOT on the S&P 500!!!


```python
# first perform the join
joined = pd.merge(left=companies, right=sandp, how="left", left_on="symbol", right_on="Symbol")

# second filter out any of the matches
not_on_sandp = joined[joined["Symbol"].isna()]
not_on_sandp
```

### 1.3 You Code

Now you try it use the `merge()` method function to join the `companies` to `sandp` but this time only show matches. If you use a different `how` you can complete this in a single step.

Save the results in a `matched` dataframe and `display()` it.


```python
# todo write code here

```

## Combining DataFrames by row.

We can use the `concat()` method function to combine rows of multiple dataframes into a single dataframe with more rows.

For example if you `contact()` three dataframes with 10, 15 and 20 rows the resulting dataframe will have 10+15+20 == 45 rows.

In this example we read in stock history for the 3 companies in the list, and append them.


```python
microsoft = pd.read_csv("stocks/MSFT.csv")
microsoft
```


```python
google = pd.read_csv("stocks/GOOG.csv")
google
```


```python
apple = pd.read_csv("stocks/AAPL.csv")
apple
```


```python
combined = pd.concat([microsoft, google, apple], ignore_index=True)
combined
```

Notice to use `concat()` the target dataframes must be in a list.

### 1.4 You Code

Let's make the previous example more efficient by using a loop. Most of this code has been written for you. You just need to write the one line of code to read in each stock inside the body of the loop.



```python
# todo: repeat the analysis in the previous cell for Pclass 
stocks = ["MSFT", "GOOG", "AAPL"]
combined = pd.DataFrame()
for stock in stocks:
    filename = f"stocks/{stock}.csv"
    # todo read the filename into `stocks_df`

    combined = pd.concat([combined, stocks_df], ignore_index=True)
combined
```

## Lambdas and apply()

The Pandas `apply()` method allows us to write a user-defined function and the invoke that function for every row in the dataframe.

This is useful when you need to implement complex transformational logic on your dataframes.

### Example

Let's predend there is an applied tax rate based on the `info.state` based on the following table:

    - NY = 0.15
    - WA = 0.10
    - CA = 0.20
    - Tx = 0.05
    - Everyone else = 0.0

We've seen before you can write this as a function:


```python
def taxrate(state: str) -> float:
    state = state.upper()
    if state == "NY":
        rate = 0.15
    elif state == "WA":
        rate = 0.1 
    elif state == 'CA':
        rate = 0.2
    elif state == 'TX':
        rate = 0.05
    else:
        rate = 0.0
    return rate

# simple test
assert taxrate("TX") == 0.05
```

With the function created we can now use `apply()` to calculate a `"tax"` column:


```python
companies["tax"] = companies.apply(lambda row: taxrate(row["info.state"]), axis=1)
companies.head()
```

#### NOTE!!!

For more details on `lambda/apply` check the assigned reading!


```python
def change(open: float, close: float) -> float:
    return close - open

assert change(1.5, 1.25) == -0.25
```

### 1.5 You Code 

Using the function `change()` as defined in the cell above, add a column to the `combined` dataframe from 1.4 called `"change"` which calculates the change in the stock for each row. `display()` the output.


```python
# todo write code here

```
