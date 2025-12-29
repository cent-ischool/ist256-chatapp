# IST256 Lesson 13
## Web API's


- Assigned Reading: [Fudge: Web APis](WebApis.ipynb)

## Links

- Participation: [https://poll.ist256.com](https://poll.ist256.com)  (Sign in with *netid*@syr.edu and your SU Password.)
- Class Chat: [https://chat.ist256.com](https://chat.ist256.com)  (Microsoft Teams.)


# Agenda

- Homework
- What is a web api / why do they exist?
- Making HTTP Requests
- Common request patterns
- Using the CENT IoT Api Wrapper


# FEQT (Future Exam Questions Training) 1

How many rows in the DataFrame?


```python
import pandas as pd
data = [
    {'A': [{"C": 1}], 'B': "x"},     
    {'A': [{"C": 3}, {"C": 2}, {"C": 4}], 'B': "y"}
]
df = pd.json_normalize(data)
df.loc[1,"B"]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>[{'C': 1}]</td>
      <td>x</td>
    </tr>
    <tr>
      <th>1</th>
      <td>[{'C': 3}, {'C': 2}, {'C': 4}]</td>
      <td>y</td>
    </tr>
  </tbody>
</table>
</div>



A. `1`  
B. `2`  
C. `3`  
D. `4`  
 
## Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# FEQT (Future Exam Questions Training) 2

How many rows in the DataFrame?


```python
import pandas as pd
data = [
    {'A': [{"C": 1}], 'B': "x"},
    {'A': [{"C": 3}, {"C": 2}, {"C": 4}], 'B': "y"}
]
df = pd.json_normalize(data, record_path="A")
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>C</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>



A. `1`  
B. `2`  
C. `3`  
D. `4`  
 
## Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# FEQT (Future Exam Questions Training) 3

What is the output of the following code?


```python
data = [
    {'A': [{"C": 1}], 'B': "x"},
    {'A': [{"C": 3}, {"C": 2}, {"C": 4}], 'B': "y"}
]
df = pd.DataFrame(data)
df.loc[0, "B"]
```

A. `X`  
B. `y`  
C. `B`  
D. `Error`  
 
## Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# FEQT (Future Exam Questions Training) 4

What is the output of the following code?


```python
data = [
    { 'A' : [{"C":1}], 'B': "x" },
    { 'A' : [{"C":3},{"C":2},{"C":4}], 'B': "y" }
]
df = pd.DataFrame(data)
df[df['B']=='x'][['A']]
```

A. `{"C":1}`  
B. `{"C":1}`  
C. `{"C":3}`  
D. `{"C":4}`  
 
## Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# FEQT (Future Exam Questions Training) 5

You want to visualize Average retail price by smartphone brand (Apple, Google, Samsung). Which is the most appopriate method?

A. `lmplot()`  
B. `lineplot()`  
C. `histplot()`  
D. `barplot()`  
 
 
## Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

 # What is a web API? 
 
 - Another form of "Other People's code"
 - This time the code is in the cloud.
 - We call the functions over the internet.
 - Why? Some code is too complex to run on our local devices.
 - Web API's are why smartphone apps like Uber, Snapchat, and Venmo are able to work.
 
    

# HTTP: The Protocol of The Web

Just another form of `INPUT -> PROCESS -> OUTPUT`

- **Request:** sent by you to the web API over the internet.
  - **URL** Uniform resource locator. Where on the internet you are requesting
  - **Query String** for simple inputs like a value or search parameters
  - **Body** for large inputs like text and images
  - **Header** for secret inputs like API Keys or access privileges.
- **response:** what you get back. Consists of:
  - **Status Code**. This indicates "what happened"
  - **Content**  this is the the result of the function call. Its in binary, text or JSON format.



# HTTP Request Methods

HTTP Request Verbs:
- GET - used to get resources
- POST - used to send large data payloads as input

Less Common:
- PUT - used for updates
- DELETE - used to delete a resource


# HTTP Response Status codes

The HTTP response has a payload of data and a status code. 

HTTP Status Codes:
- `1xx` Informational -seldome used in API's
- `2xx` Success - it worked
- `3xx` Redirection - its no longer there or hasn't changed
- `4xx` Client Error - you make a mistake
- `5xx` Server Error - they made a mistake

# Python requests

Python's `requests` module makes calling web API's simple. The process is always the same:

1. Setup the inputs: Query String, Body or Header
2. Make the GET or POST to the URL
3. Check for non 200 response
4. when valid, Proceed reading the response content


# Watch Me Code 1 

Funny Names with Python requests:

- https://cent.ischool-iot.net/api/funnyname/random
- https://cent.ischool-iot.net/api/funnyname/search
- learn to use query string
- handling errors
- deserializing JSON


# Check Yourself: Response Codes

The HTTP Response meaning is your fault is:  
A. `404`  
B. `501`  
C. `200`  
D. `301`  

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# CENT IoT Portal

- Center for Emerging Network Technologies portal for Internet of Things
- We will use in this class for web API calls
- There are wrappers on common API's to keep them stable and easy for you to access.
- Login with your netid.

https://cent.ischool-iot.net


# Watch Me Code 2

 - CENT IoT portal
 - Get your API Key
 - Swagger Docs so you can try API's
 - Let's call the geocode and weather api's
 - Converting a CURL to Python requests


# Check Yourself : HTTP Methods


What is the URL printed on the last line?


```python
import requests
params = { 'a' : 1, 'b' : 2 }
headers = { 'c' : '3'}
url = "https://httpbin.org/get"
response = requests.get(url, params = params, headers = headers)
print(response.url)
```

A. `https://httpbin.org/get?a=1&b=2&c=3`  
B. `https://httpbin.org/get?a=1&b=2`  
C. `https://httpbin.org/get?c=3`  
D. `https://httpbin.org/get`  


### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)

# End-To-End Example:

### Today's Weather

- Lets combine weather + geocoding API's into a single example


# Conclusion Activity: Exit Ticket 

Which HTTP method is used to send large quantities of data to the URL?

A. `GET`  
B. `POST`  
C. `DELETE`  
D. `PUT`   

### Vote Now: [https://poll.ist256.com](https://poll.ist256.com)
