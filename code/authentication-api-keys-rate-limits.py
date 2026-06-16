# Authentication, API Keys, and Rate Limits

##  Introduction to API Authentication

import requests

url = "https://api-server.dataquest.io/private/historical_data"

response = requests.get(url)

print(response.status_code) # 401

## Navigating API Documentation

"""

Our API offers a comprehensive guide to effectively utilizing its features. Here's what we need to know:

Base URL: The primary access point for the API is https://api-server.dataquest.io/economic_data. This URL serves as the foundation to which endpoint paths are appended. For private tables, we will use https://api-server.dataquest.io/private/economic_data.

Endpoints: The API provides various endpoints, such as /indicators, /countries, /historical_data, /footnote, /country_series, and /series_time. These endpoints represent different data resources accessible through the API.

HTTP Methods: Our API primarily responds to GET requests, allowing users to retrieve data from the specified endpoints.

Parameters: Parameters like limit, offset, field, filter_by, sort_by, and sort_desc can be used to refine data retrieval, offering control over the quantity, pagination, and sorting of the data.

Response Formats: The API delivers responses as JSON-formatted strings, specifically as lists of dictionaries enclosed in quotes. To convert these strings into usable list formats in Python, you can use json.loads(). This approach ensures that the data is both user-friendly and easily parsed for practical utilization.

Rate Limits: Most APIs impose limits on the number of requests you can make in a certain timeframe to prevent abuse and ensure fair usage.

Error Messages: Our API is designed to handle various error scenarios effectively, providing clear messages to aid in troubleshooting. Here are some potential error cases and their corresponding messages:

Authentication Errors: If a request to a private endpoint lacks proper authentication, the API responds with "Unauthorized" or "Invalid authentication credentials". This occurs when the 'Authorization' header is missing, incorrect, or if the provided credentials do not match our records.

Database and Table Validation: When a request is made for a non-existent database or table, the API raises a "Selected database does not exist" or "Selected table does not exist" error. This ensures users are querying valid data sources.

Invalid Query Parameters: If query parameters like field, filter_by, or sort_by contain values not present in the database schema, the API responds with "Invalid [parameter] parameter, please ensure that only fields available in schema are specified."

Filter Syntax Errors: Incorrect filter syntax, particularly with comparators, triggers a "Incorrect filter comparator, please use one of the following: =, !=, ~" error message.

Access Violations: Attempts to access private data without proper authorization, or using the public API for private data, result in "Not authorized" or "Please use public API to retrieve data from a public source" messages.

General Exceptions: For other unforeseen errors, the API provides a generic "Unknown error occurred" message. This is a catch-all response for exceptions not explicitly handled by the API.

Authentication: Access to private endpoints requires authentication, which is supported through two methods: basic authentication and token-based authentication. For basic authentication, use the header Authorization: Basic <base64-encoded credentials>. For token-based authentication, use Authorization: Bearer <token>.

"""

## Basic Authentication

import base64
import requests
username = "dq"
password = "test"


encoded_credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

url = "https://api-server.dataquest.io/private/economic_data/historical_data"
headers = {
    'Authorization': f'Basic {encoded_credentials}'
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    response_preview=response.text[:500]
    print("Response Preview:", response_preview)


##  Environment Variable

"""
Let's consider some risks associated with exposed credentials in Basic Authentication:

Unauthorized Access: Exposed credentials can lead to unauthorized access to APIs, potentially leading to data breaches.

Data Manipulation: If someone else gets hold of your credentials, they could manipulate the data you are accessing or modifying through the API.

Service Abuse: Misuse of your credentials could result in the abuse of the API services, affecting your application's functionality and possibly incurring additional costs.

Reputation Damage: Misuse of credentials under your name could negatively impact your or your organization's reputation.
"""

## Troubleshooting: Handling Authentication Errors

"""
400 Bad Request: This status code indicates that the request sent to the server was incorrect or corrupted and the server couldn't understand it. It often points to issues such as improperly formatted request syntax, invalid request message parameters, or deceptive request routing.

401 Unauthorized: This means the request lacks valid authentication credentials for the target resource. In other words, our API key was invalid, and we've been denied access.

403 Forbidden: This means the server understood the request, but it refuses to authorize it. This status is similar to 401 (Unauthorized), but indicates that the client must authenticate itself to get the requested response.

429 Too Many Requests: This means the user has sent too many requests in a given amount of time ("rate limiting"). In this case, we've exceeded our quota and need to slow down.
"""

### create an error:

import requests
import base64

url = "https://api-server.dataquest.io/private/economic_data/historical_data"

username = "sq" # dq
password = "tester" # test

encoded_credentials = base64.b64encode("f{username}:{password}".encode()).decode()

headers = {
    'Authorization': f'Basic {encoded_credentials}'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")  # Handling specific HTTP error
    
# --> HTTP error occurred: 401 Client Error: Unauthorized for url: https://api-server.dataquest.io/private/economic_data/historical_data    


## Understanding API Rate Limits and Quotas
# When you exceed an API's quota (max requests per time period) or rate limit (number of requests in time period t), the server typically responds with a 429 Too Many Requests HTTP status code.


"""
import requests
import time
import base64

# Setting up Basic Authentication
username = 'dq'
password = 'test'
encoded_credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
headers = {'Authorization': f'Basic {encoded_credentials}'}

url = 'https://api-server.dataquest.io/private/economic_data/historical_data'

# Attempting to send multiple requests to demonstrate exceeding the quota or rate limit
for i in range(1001):
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code == 429:
        print("Rate limit exceeded. Waiting for 60 seconds before next request.")
        time.sleep(60)  # Waiting for 1 minute before making the next 
"""

##  Timing API Requests

"""
Let's say we're working with an API that has a rate limit of 100 requests per minute. To stay within this limit, we could add a delay of 0.6 seconds (60 seconds / 100) between each request. Here's an example:

import requests
import time

url = 'https://api-server.dataquest.io/private/economic_data/footnotes'
username = 'dq'
password = 'test'
encoded_credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
headers = {'Authorization': f'Basic {encoded_credentials}'}

for i in range(100):
    response = requests.get(url, headers=headers)
    print(response.status_code)
    time.sleep(0.6)
"""

## Dealing with Rate Limit

"""
import requests
import time

url = 'https://api-server.dataquest.io/private/economic_data/footness'

username = 'dq'
password = 'test'
encoded_credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
headers = {'Authorization': f'Basic {encoded_credentials}'}

for i in range(101): # Sending 101 requests to demonstrate the rate limit error
    response = requests.get(url, headers=headers)
    if response.status_code == 429:  # If we hit the rate limit
        print("Rate limit exceeded. Waiting for 60 seconds before next request.")
        time.sleep(60)  # Pause the script for 60 seconds
    else:
        print(response.status_code)
    time.sleep(0.6)  # Pause for 0.6 seconds between requests to respect the rate limit
"""

## Understanding API Key Authentication

"""
import requests

# Hypothetical URL for an API that supports API key authentication
url = 'https://api.example.com/data'
headers = {'Authorization': 'Bearer YOUR_API_KEY'}

# Making a request with the API key
response = requests.get(url, headers=headers)
print(response.json())
"""