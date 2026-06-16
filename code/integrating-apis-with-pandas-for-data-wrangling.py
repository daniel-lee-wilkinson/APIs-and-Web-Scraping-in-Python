# Integrating APIs with Pandas for Data Wrangling

##  Creating a DataFrame from JSON Data

import pandas as pd

json_data = '{"country": ["Canada", "England", "Japan"], "region": ["North America", "Europe", "Asia"]}'

df_country = pd.read_json(json_data)
df_total_rows = len(df_country)
print(df_country)
print(df_total_rows)

## Data Formats in API Retrieval

import requests
url = "https://api-server.dataquest.io/economic_data/countries"
response = requests.get(url)
economic_data = response.json()


print(economic_data)

## Reading JSON Data into a DataFrame

import pandas as pd
import requests


response=requests.get('https://api-server.dataquest.io/economic_data/indicators')
data = response.json()
df_economic = pd.read_json(data)
most_frequent_source =df_economic['source'].value_counts().idxmax()
print(most_frequent_source)



## Handling Data without APIs

import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://dataquestio.github.io/web-scraping-pages/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table')
df= pd.read_html(str(table))[0]
df_columns=len(df.columns)
print(df_columns)


## Exploring HTML Pages

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://dataquestio.github.io/web-scraping-pages/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

link_texts=[]
link_hrefs=[]

for link in soup.find_all('a'):
    link_texts.append(link.get_text().strip())
    link_hrefs.append(link.get('href'))

links_dict = {'Link Text': link_texts, 'URL': link_hrefs}
    
df_links=pd.DataFrame(links_dict)
print(df_links.head())


##  Data Analysis with DataFrames

import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://dataquestio.github.io/web-scraping-pages/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table')
df_wikipedia = pd.read_html(str(table))[0]


print(df_wikipedia.info())
df_wikipedia = df_wikipedia.drop(columns=['Unnamed: 0'], errors='ignore')
cleaned_df = df_wikipedia.drop_duplicates()
print(cleaned_df.describe())


## Advanced Data Analysis with DataFrames

import matplotlib.pyplot as plt

# Our cleaned DataFrame. Uncomment the following if you want to use it:
df_wikipedia = df_wikipedia.drop(columns=['Unnamed: 0'], errors='ignore')
df_wikipedia = df_wikipedia.drop_duplicates()
countries_pop_under_10000=df_wikipedia[df_wikipedia['Population']<10000]
countries_pop_under_10000=countries_pop_under_10000[countries_pop_under_10000['Location'] != 'World']

countries_pop_under_10000.plot(kind='barh', x='Location', y='Population')
plt.xlabel('Population')
plt.ylabel('Location')
plt.title('Population by Country')
plt.show()

