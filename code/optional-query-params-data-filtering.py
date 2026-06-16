# Further Exploration of Query Parameters in APIs

# World bank Development Indicators database_link: https://datatopics.worldbank.org/world-development-indicators/
# these parameters are supported: /countries, /indicators, /country_series, /series_time, /footnotes, and /historical-data.
# DQ s side server: https://api-server.dataquest.io/economic_data

# %20 is URL encoding for a space character, necessary because URLs cannot contain actual space characters. However, when composing a GET request in an editor or a tool, you don't need to manually type %20 for spaces; it is typically handled automatically by the software.

import requests
import json


response = requests.get("https://api-server.dataquest.io/economic_data/countries?filter_by=region=South Asia")
region_south_asia = response.json()
print(region_south_asia)

# Multiple Query Parameters

response=requests.get("https://api-server.dataquest.io/economic_data/indicators?filter_by=topic=Health: Risk factors&filter_by=periodicity=Biennial")
topic_str = response.json()
topic=json.loads(topic_str)
for row in topic:
    print(f"indicator Code: {row['series_code']}")
    print(f"Indicator Name: {row['indicator_name']}")
    break
    
# Handling Invalid Parameter Values

response = requests.get("https://api-server.dataquest.io/economic_data/indicators?filter_by=indicator_period=Biennial")
invalid_data_str = response.json()
print(invalid_data_str)
    
    
#--> {'detail': 'Invalid filter_by parameter, please ensure that only fields available in schema are specified.'}


# Error Handling in API Requests
## In Python programming, these errors can be managed using try/except blocks. When code within a try block encounters an error, Python shifts to the except block, allowing the programmer to handle the error or provide alternative instructions. This mechanism ensures that the program can gracefully manage unexpected situations or errors during execution.


# Pagination in API Requests
## Pagination in APIs is a technique used to divide the data into smaller, manageable segments or pages. 
## While other APIs use page and per_page parameters for pagination, our side API server employs limit and offset. Here's how they work:

parameters = {
    "limit": 10,
    "offset": 0
}
base_url = "https://api-server.dataquest.io/economic_data"
endpoint = "/countries"
url = f"{base_url}{endpoint}"
response = requests.get(url, params = parameters)
data_with_pagination  = json.loads(response.json())
print(len(data_with_pagination))

# Implementing Pagination

"""
A typical API response supporting pagination might have a structure like: 
{
    "page": 1,
    "per_page": 10,
    "total": 100, # total number of records available
    "total_pages": 10, # total number of pages calculated on the per_page parameter
    "data": [...]
}

Alternative types of pagination:
- cursor-based pagination
parameters = {
    "cursor": "abc123"
}
- keyset pagination
parameters = {
    "start_after": "2021-01-01T12:00:00Z"
}
"""

parameters = {"limit": 10, "offset": 0}

response = requests.get("https://api-server.dataquest.io/economic_data/indicators", params = parameters)

indicator_page_str = response.json()
indicator_page = json.loads(indicator_page_str)
indicator_len_records = len(indicator_page)

fourth_indicator_name = indicator_page[3].get("indicator_name", [])
print(indicator_len_records)
print(fourth_indicator_name)


# Optimizing Pagination

parameters = {
    "limit": 50,  
    "offset": 0   
}
response = requests.get("https://api-server.dataquest.io/economic_data/indicators", params=parameters)
data_page_1 = json.loads(response.json())
print("Limit (total records):", len(data_page_1))
print("First topic:", data_page_1[0].get("topic", []))
parameters["offset"] = 50
response = requests.get("https://api-server.dataquest.io/economic_data/indicators", params=parameters)
data_page_2 = json.loads(response.json())
print("New topic:",data_page_2[0].get("topic", []))


# Combining Query Parameters and Pagination

parameters = {
"filter_by":"region=Europe & Central Asia,income_group=Upper middle income",
"limit":5,
"offset":0}


url = "https://api-server.dataquest.io/economic_data/countries"

response = requests.get(url, params=parameters)

data_combined_str = response.json()

data_combined = json.loads(data_combined_str)

for record in data_combined:
    country_name=record.get("table_name")
    print(country_name)
    
# Pagination with Page and Page_Number in API Requests

""" EXAMPLE 
import requests


# Set base URL and endpoint
base_url = "https://api-server.dataquest.io/economic_data"
endpoint = "/historical_data"

# Set query parameters with pagination
parameters = {
    "country_code": "IND",
    "indicator_code": "SP.POP.TOTL",
    "from_year": 2000,
    "to_year": 2020,
    "page": 1,         # Current page number
    "page_number": 50  # Number of records per page
}

# Send GET request
response = requests.get(base_url + endpoint, params=parameters)
data = response.json()

# Print first 5 records
print(data["records"][:5])

# Handling total number of records
total_records = data["total"]
print(f"Total records available: {total_records}")
"""


