import requests

endpoint_url = 'https://api.exchangerate-api.com/v4/latest/gbp'
response = requests.get(endpoint_url)
response_dict = response.json()

print(type(response))
print(type(response_dict))

for key in response_dict:
    print(key, ":", response_dict[key])

# GET Method: retrieve data from a server
# Query parameters are appended to the URL using the ? symbol, followed by key-value pairs separated by &.
# GET Method does not require a request body. All necessary info is passed through the URL and query parameters instead.

import requests

currencies = ['EGP', 'GMD', 'CLP']
base_url = "https://api.exchangerate-api.com/v4/latest/"

for currency in currencies:
    url = base_url + currency
    response = requests.get(url)
    response = response.json()
    print(response['rates']['USD'])

# POST Method: 

"""
------- EXAMPLE (INACTIVE) POST REQUEST:---------------
# Define the API endpoint URL where the account creation information will be submitted
endpoint = "https://example.com/api/create-account"
​
# Prepare the account creation data as a dictionary
account_data = {
    "username": "example_user",
    "email": "example@example.com",
    "password": "example_password"
}
​
# Make the POST request to submit the account creation data
response = requests.post(endpoint, json=account_data)

# see post.svg image
"""

# Converting JSON Data to Strings
# see json-dump-post.svg

exchange_rate_map = {
    'EUR': 0.927,
    'USD': 1,
    'CAD': 1.33,
    'JPY': 139.9,
    'GBP': 0.794
}
print(type(exchange_rate_map))

import json

exchange_rate_map_str = json.dumps(exchange_rate_map)
print(exchange_rate_map_str)
print(type(exchange_rate_map_str))


# Formatting Strings

# although f-strings can be very useful for string formatting, the json.dumps() function is often a better choice
# when working with more complex data structures because it automatically handles special characters and escape sequences.

import requests

currencies = ['EGP', 'GMD', 'CLP']
base_url = "https://api.exchangerate-api.com/v4/latest/"


for currency_code in currencies:
    url = f"{base_url}{currency_code}"
    response = requests.get(url)
    response = response.json()
    print(f'The exchange rate from {currency_code} to USD is {response["rates"]["USD"]}.')


# HTTP Request Error Handling

# ERROR CODES
"""
Code	Status	Description
200	OK	Successful request
201	Created	Successful request, new resource created (occurs with a PUT request)
400	Bad Request	Request syntax or parameters are incorrect
401	Unauthorized	Authentication required or credentials are invalid
404	Not Found	Requested resource does not exist (for example, the endpoint does not exist
500	Internal Server Error	An error occurred on the server side

"""

import requests

currency_codes = ['cad', 'abc']
base_url = "https://api.exchangerate-api.com/v4/latest/"

for currency_code in currency_codes:
    url = f"{base_url}{currency_code}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        print("Request was successful!")
    elif response.status_code == 404:
        print("Endpoint not found!")