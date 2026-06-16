# Guided Project: Exploring Financial Data using Nasdaq Data Link API
# Goal: Detailed analysis of financial data, including trend analysis and comparative studies.

import requests
import matplotlib.pyplot as plt
import config
import pandas as pd

api_key = config.API_KEY

# Rate limits: 300 calls per 10 seconds, 20000 per 10 minutes, 50000 calls per day

api_url = "https://data.nasdaq.com/api/v3/datatables/MER/F1.json"

parameters = {
    'api_key': api_key,
    'qopts.per_page': 10000
}

response = requests.get(api_url, params=parameters)
json_data = response.json()

# Processing the JSON Data into a DataFrame
data = json_data['datatable']['data']
columns = [col['name'] for col in json_data['datatable']['columns']]
df_metric = pd.DataFrame(data, columns=columns)

print(df_metric.info())

necessary_columns = [
    'reportid',
    'reportdate',
    'reporttype',
    'amount',
    'longname',
    'country',
    'region',
    'indicator',
    'statement'
]

df_metric = df_metric[necessary_columns]
print(df_metric["indicator"].unique())

# Mappings and helpers
country_mapping = {
    'USA': 'United States of America',
    'DEU': 'Germany',
    'JPN': 'Japan',
    'CYM': 'Cayman Islands',
    'BHS': 'Bahamas',
    'IRL': 'Ireland',
    'GBR':'United Kingdom'
}

def update_country_name(name):
    return country_mapping.get(name, name)  # falls back to original name if not found

def transform_df(df):
    df = df.copy()
    df["country_name"] = df["country"].apply(update_country_name)
    df = df.rename(columns={
        'longname': 'company_name',
        'reportdate': 'report_date',
        'reporttype': 'report_type',
        'reportid': 'report_id',
    })
    df['report_date'] = pd.to_datetime(df['report_date'])
    df = df[(df['report_date'].dt.year >= 2010) & (df['report_date'].dt.year <= 2025)]
    return df

# --- Accrued Expenses Turnover Analysis ---
filtered_df = df_metric[df_metric['indicator'] == 'Accrued Expenses Turnover']
updated_df = transform_df(filtered_df)

print(updated_df["indicator"].describe())
print(updated_df["country_name"].value_counts())

# Trend Analysis
relevant_data = updated_df[["company_name", "report_date", "amount"]]
print(relevant_data.head())

plt.figure(figsize=(12, 6))
for company in relevant_data["company_name"].unique():
    company_data = relevant_data[relevant_data["company_name"] == company]
    plt.plot(company_data["report_date"], company_data["amount"], label=company)

plt.title('Trend Analysis of Accrued Expenses Turnover (2010-2015)')
plt.xlabel('Report Date')
plt.ylabel('Accrued Expenses Turnover')
plt.xticks(rotation=45)
plt.legend(title='Company', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
#plt.show()

# Geographical Region Analysis
country_avg = updated_df.groupby('country_name')['amount'].mean()
plt.figure(figsize=(12, 6))
country_avg.sort_values(ascending=False).plot(kind='bar')
plt.title('Average Financial Metric by Country')
plt.xlabel('Country')
plt.ylabel('Average Amount')
plt.xticks(rotation=45)
plt.tight_layout()
#plt.show()

# --- Extension: Efficiency Indicators ---
efficiency_df = df_metric[df_metric['indicator'].isin(["Total Asset Turnover", "Total Revenue", "Net Margin"])]
efficiency_df = transform_df(efficiency_df)

print(efficiency_df["country_name"].unique())

print(efficiency_df.groupby(["indicator", "company_name"])["amount"].describe())
companies = efficiency_df["company_name"].unique()
indicators = efficiency_df["indicator"].unique()

fig, axes = plt.subplots(len(indicators), len(companies), figsize=(18, 12), sharey=False)

for i, indicator in enumerate(indicators):
    for j, company in enumerate(companies):
        ax = axes[i, j]
        data = efficiency_df[(efficiency_df["indicator"] == indicator) &
                             (efficiency_df["company_name"] == company)]

        ax.plot(data["report_date"], data["amount"])
        ax.set_title(f"{company}\n{indicator}", fontsize=8)
        ax.tick_params(axis='x', rotation=45)
        ax.set_xlabel('Report Date', fontsize=7)
        ax.set_ylabel('Amount', fontsize=7)

plt.suptitle('Efficiency Indicators by Company (2010-2015)', y=1.02)
plt.tight_layout()
fig.savefig("efficiency_indicators.png", dpi=150, bbox_inches='tight')

print(efficiency_df[efficiency_df["company_name"] == "Ultrapetrol (Bahamas) Ltd"]["report_date"].unique())
efficiency_df_filtered = efficiency_df[efficiency_df["country_name"].isin(["Germany", "United Kingdom"])]

companies = efficiency_df_filtered["company_name"].unique()
indicators = efficiency_df_filtered["indicator"].unique()

print(efficiency_df_filtered["company_name"].unique())
print(efficiency_df_filtered["country_name"].unique())
print(len(efficiency_df_filtered))
print(df_metric[df_metric['country'].isin(['GBR', 'DEU'])][['longname', 'indicator']].drop_duplicates())
fig, axes = plt.subplots(len(indicators), len(companies), figsize=(18, 12), sharey=False, squeeze=False)
for i, indicator in enumerate(indicators):
    for j, company in enumerate(companies):
        ax = axes[i, j]
        data = efficiency_df_filtered[(efficiency_df_filtered["indicator"] == indicator) &
                             (efficiency_df_filtered["company_name"] == company)]

        ax.plot(data["report_date"], data["amount"])
        ax.set_title(f"{company}\n{indicator}", fontsize=8)
        ax.tick_params(axis='x', rotation=45)
        ax.set_xlabel('Report Date', fontsize=7)
        ax.set_ylabel('Amount', fontsize=7)

plt.suptitle('Efficiency Indicators by Company - Germany & UK (2010-2016)', y=1.02)
plt.tight_layout()
fig.savefig("efficiency_indicators_DE_UK.png", dpi=150, bbox_inches='tight')