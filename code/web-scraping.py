# Web Scraping

## Practical Applications of Web Scraping

"""
Uses: data journalism, e-commerce, recruitment,social media, SEO Monitoring, research

EXAMPLE:

# Import necessary libraries
import requests
from bs4 import BeautifulSoup

# Send an HTTP request to the URL of the webpage
response = requests.get('https://dataquestio.github.io/web-scraping-pages/')

# Parse the content of the request
soup = BeautifulSoup(response.text, 'html.parser')

# Find the main table using the class attribute
table = soup.find('table', {'class': 'wikitable'})

# Find all rows in the table
rows = table.find_all('tr')

# Loop through each row
for row in rows:
    # Find all columns in each row
    cols = row.find_all('td')
    # Get the text from each column
    cols = [col.text.strip() for col in cols]
    # Print the columns
    print(cols)
"""

import requests
from bs4 import BeautifulSoup

WEB_SCRAPING_PAGES_ = "https://dataquestio.github.io/web-scraping-pages/"


def extract_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class":"wikitable"})
    rows = table.find_all("tr")
    data = []
    for row in rows:
        cols = row.find_all("td")
        cols = [col.text.strip() for col in cols]
        data.append(cols)
    return data

url = WEB_SCRAPING_PAGES_
population_data = extract_data(url)
print(population_data[:5])


## Extracting Data from Web Pages

import requests
from bs4 import BeautifulSoup

response = requests.get(WEB_SCRAPING_PAGES_)

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", {"class":"wikitable"})

rows = table.find_all("tr")

top_100_countries = rows[2:102]
for row in top_100_countries:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        print(cols)


##  Handling Errors and Exceptions in Web Scraping

"""
There are two types of errors we typically encounter when web scraping:

Connection Errors: These occur when there is a network problem, like a DNS failure (when the domain name cannot be converted into its corresponding IP address) or a refused connection (when the server refuses to respond). A common exception for this is requests.exceptions.RequestException.

HTTP Errors: These occur when an HTTP request returns an unsuccessful status code. For example, a 404 Not Found error means that the requested resource could not be found on the server, and a 500 Internal Server Error means that the server encountered an unexpected condition. A common exception for this is requests.exceptions.HTTPError.
"""

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, HTTPError

url = WEB_SCRAPING_PAGES_
try:
    response=requests.get(url)
    response.raise_for_status()
except RequestException as e:
    print(f"There was an issue with your request: {e}")
except HTTPError as e:
    print(f"HTTP error occurred: {e}")
    
soup=BeautifulSoup(response.text, "html.parser")
table=soup.find("table", {"class":"wikitable"})
rows = table.find_all("tr")

top_20_countries=rows[2:22]

for row in top_20_countries:
    cols=row.find_all("td")
    cols = [col.text.strip() for col in cols]
    print(cols)
    
## Understanding HTML Elements, IDs, and Classes

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, HTTPError

url = WEB_SCRAPING_PAGES_
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

table=soup.find("table", {"class":"wikitable"})
print(table)


## Applying CSS Selectors for Targeted Data Extraction

"""
# Select elements with the class 'history'
history_elements = soup.select('.history')

# Select the element with the id 'book_123'
book_123 = soup.select('#book_123')

# Select all `p` elements inside `div` elements
div_paragraphs = soup.select('div p')

td_elements = td_elements[13:]  # The first two rows are unstructured, so we start at the 14th element, assuming the 3rd row onwards.

# Loop through each 'td' element
for i in range(len(td_elements)):
    # If the index of the 'td' element is 3 (which corresponds to the 'Date' column)
    if i % 6 == 3:
        # Extract the text from the 'td' element and print it
        date = td_elements[i].text
        print(date)
"""

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, HTTPError

url = WEB_SCRAPING_PAGES_

try:
    response=requests.get(url)
    response.raise_for_status()
except RequestException as e:
    print(f"There was an issue with your request: {e}")
except HTTPError as e:
    print(f"HTTP error occurred: {e}")

soup=BeautifulSoup(response.text, "html.parser")
td_elements = soup.select("tr td")
td_elements=td_elements[12:]
population_list=[]
for i in range(len(td_elements)):
    if i % 6 ==1:
        population=td_elements[i].text
        population_list.append(population)

print(population_list[:10])

## Handling Different Data Types in Web Scraping

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, HTTPError
from datetime import datetime


try:
    response = requests.get(WEB_SCRAPING_PAGES_)
    response.raise_for_status()
except RequestException as e:
    print(f"There was an issue with your request: {e}")
except HTTPError as e:
    print(f"HTTP error occurred: {e}")
soup = BeautifulSoup(response.text, 'html.parser')
td_elements = soup.select('tr td')
td_elements = td_elements[12:]
first_30_rows = 0
for i in range(len(td_elements)):
    if i % 6 == 0:
        first_30_rows += 1
    if first_30_rows > 30:
        break
    if i % 6 == 1:
        population = td_elements[i].text
        population = int(population.replace(',', ''))
        print(population)
    elif i % 6 == 2:
        percentage = td_elements[i].text
        percentage = float(percentage.replace('%', ''))
        print(percentage)    
    elif i % 6 == 3:
        date = td_elements[i].text
        date=date.strip() 
        try:
            date = datetime.strptime(date, '%d %b %Y')
            print(date)
        except ValueError:
            print("Date not found")

## Storing and Structuring Scraped Data

# Store the data as a pandas dataframe, then export to csv

"""
data = [['China', '1,411,750,000', '17.5%', '31 Dec 2022', 'Official estimate[4]', '[b]'], ['India', '1,392,329,000', '17.3%', '1 Mar 2023', 'Official projection[5]', '[c]'], ['United States', '335,495,000', '4.2%', '11 Oct 2023', 'National population clock[7]', '[d]']]

import pandas as pd

# Define the column names
columns = ['Country/Dependency', 'Population', '% of World', 'Date', 'Source', 'Notes']

# Create a DataFrame from the data
df = pd.DataFrame(data, columns=columns)

# Write the DataFrame to a CSV file
df.to_csv('population_data.csv', index=False)
print(df)

"""
