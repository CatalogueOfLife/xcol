#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 12:07:29 2024
Update: 2025-02-06

@author: camisilver
"""

import requests # For API calls
from requests.auth import HTTPBasicAuth # For API calls that need authentication
import pandas as pd
# pip install aiohttp
import aiohttp 
import asyncio #To improve API performans, asyncronus calls
#pip install nest_asyncio
import nest_asyncio
nest_asyncio.apply()
import time
from datetime import datetime



# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")
username = 
password = 
#username = 
#password = 

# API endpoint
url = "https://api.checklistbank.org/dataset?limit=1&releasedFrom=3&reverse=true"
# authentication
response = requests.get(url, auth=(username, password))
response.raise_for_status()  # Raise an error for bad responses
# Parse JSON response
data = response.json()
# Extract the 'key' value
if "result" in data and isinstance(data["result"], list) and len(data["result"]) > 0:
    dataset_key = data["result"][0].get("key")
    print("Extracted key:", dataset_key)
else:
    dataset_key = None
    print("No key found in response")

# Store the key in a variable
this_release_id= dataset_key

# Improvements
# - Don't relay in limit/offset to get latest releases seek for more consistent parameters
# - 


#### STEP 1
#Extract basic information from all the releases of COL Project id# 3
# Have to check if limit / offset combination is usefull
url = 'https://api.checklistbank.org/dataset?limit=20&offset=52&releasedFrom=3'
#url = 'https://api.dev.checklistbank.org/dataset?limit=50&offset=0&releasedFrom=3'
response = requests.get(url, auth=HTTPBasicAuth(username, password))

# Check the response
if response.status_code == 200:
    data = response.json()  # Parse JSON response into a dictionary
    
    # Check if 'result' key exists
    if 'result' in data:
        releases_lists = data['result']  # Extract the list of 'result' items
        
        # Extract desired fields for each JSON list and store in a list of dictionaries
        extracted_data = []
        for release in releases_lists:
            release_data = {
                'alias': release.get('alias'),
                'attempt': release.get('attempt'),
                'issued': release.get('issued'),
                'key': release.get('key'),
                'origin': release.get('origin'),
                'url': release.get('url')
            }
            extracted_data.append(release_data)
        
        # Create DataFrame from the list of dictionaries and name it "releases"
        releases = pd.DataFrame(extracted_data)
        print(releases)  # Print the DataFrame
    else:
        print('No result found in the response')
else:
    print('Request failed with status code:', response.status_code)

    
# Get entries where 'origin' is equal to 'xrelease' and  the latest 'release' (for comparisons)
# Keep only the two more recent xreleases
xrelease_df = releases[releases['origin'] == 'xrelease'].sort_values(by='issued', ascending=False).head(2) 
# Keeo only the more recent abse release
release_df = releases[releases['origin'] == 'release'].sort_values(by='issued', ascending=False).head(1) 
releases_a= pd.concat([xrelease_df, release_df]) #DataFrame with all releases



#### STEP 2
### For every release  extract needed metrics

## STEP 2.1
metrics_dict = {} # Initialize an empty dictionary

for key in releases_a['key']: # Iterate over the 'key' column of the DataFrame
    # Construct the API URL with the key
    api_url = f"https://api.checklistbank.org/dataset/{key}/import?state=finished"
    
    # API call with Basic Authentication
    response = requests.get(api_url, auth=HTTPBasicAuth(username, password))
    
    # Check if the API call was successful
    if response.status_code == 200:
        metrics_dict[key] = response.json()         # Store the information in the dictionary
    else:
        print(f"Failed to retrieve information for key: {key}")

## STEP 2.2
# Iterate over items in metrics_dict to extract general counts at the top level of the json
for key, value in metrics_dict.items():
    # Extract nameCount and synonymCount from the first item in the list
    if value:  # Check if the list is not empty
        first_item = value[0]
        name_count = first_item.get('nameCount')
        synonym_count = first_item.get('synonymCount')
        
        # Update releases_a DataFrame with nameCount and synonymCount for the corresponding key
        releases_a.loc[releases_a['key'] == key, 'nameCount'] = name_count
        releases_a.loc[releases_a['key'] == key, 'synonymCount'] = synonym_count
    else:
        print(f"No data found for key: {key}")

## STEP 2.2
# Iterate over items in metrics_dict to extract issues
issues = pd.DataFrame(columns=['key', 'Issue Type', 'Count'])

# Iterate over items in metrics_dict
for key, value_list in metrics_dict.items():
    # Check if value is a list and not empty
    if isinstance(value_list, list) and value_list:
        # Assuming you want the first item in the list
        value_dict = value_list[0]
        # Check if value_dict is a dictionary and contains 'issuesCount'
        if isinstance(value_dict, dict) and 'issuesCount' in value_dict:
            issues_count_dict = value_dict['issuesCount']
            
            # Append data to the DataFrame
            for issue_type, count in issues_count_dict.items():
                issues = pd.concat([issues, pd.DataFrame([{'key': key, 'Issue Type': issue_type, 'Count': count}])], ignore_index=True)
        else:
            print(f"No issue count data found for key: {key}")
    else:
        print(f"No data found or empty list for key: {key}")

issues = issues.pivot_table(index='key', columns='Issue Type', values='Count', fill_value=0)
issues.reset_index(inplace=True) # Reset the index
issues = pd.merge(issues, releases_a[['key', 'alias', 'issued','origin']], on='key', how='left')
issues = issues.sort_values(by='origin', ascending=True)



## STEP 2.3
# Iterate over items in metrics_dict to extract data from the sub dict "namesByRankCount" and store desired metrics
# ranks needed for 2.3 and 2.4
ranks = ['species', 'variety', 'genus', 'subspecies', 'form', 'unranked', 'family', 'other']

# Iterate over items in metrics_dict
for key, value in metrics_dict.items():
    # Extract namesByRankCount sub-dictionary
    names_by_rank_count = value[0].get('namesByRankCount') if value else None
    
    if names_by_rank_count:
        # Initialize a dictionary to store the counts
        counts = {rank: names_by_rank_count.get(rank, 0) for rank in ranks}
        
        # Update releases_a DataFrame with counts for the corresponding key
        for rank, count in counts.items():
            releases_a.loc[releases_a['key'] == key, rank + 'Names'] = count
    else:
        print(f"No data found for key: {key}")


## STEP 2.4
## Iterate over items in metrics_dict to extract data from the sub dict "taxaByRankCount" and store desired metrics

# Iterate over items in metrics_dict
for key, value in metrics_dict.items():
    # Extract taxaByRankCount sub-dictionary
    taxa_by_rank_count = value[0].get('taxaByRankCount') if value else None
    
    if taxa_by_rank_count:
        # Initialize a dictionary to store the counts
        counts = {rank: taxa_by_rank_count.get(rank, 0) for rank in ranks}
        
        # Update releases_a DataFrame with counts for the corresponding key
        for rank, count in counts.items():
            releases_a.loc[releases_a['key'] == key, rank + 'Taxa'] = count
    else:
        print(f"No data found for key: {key}")


## STEP 2.5
## Iterate over items in metrics_dict to extract data from the dict "usagesByStatusCount" and store desired metrics

statuses = ['accepted', 'synonym', 'ambiguous synonym', 'provisionally accepted', 'misapplied']

# Iterate over items in metrics_dict
for key, value in metrics_dict.items():
    # Extract usagesByStatusCount sub-dictionary
    usages_by_status_count = value[0].get('usagesByStatusCount') if value else None
    
    if usages_by_status_count:
        # Initialize a dictionary to store the counts
        counts = {status: usages_by_status_count.get(status, 0) for status in statuses}
        
        # Update releases_a DataFrame with counts for the corresponding key
        for status, count in counts.items():
            releases_a.loc[releases_a['key'] == key, status + 'status'] = count
    else:
        print(f"No data found for key: {key}")
        


#### STEP 3
# API calls to extract duplicates information

# Function to make asynchronous API requests
async def fetch(session, url, auth):
    async with session.get(url, auth=auth) as response:
        return await response.json()

# Function to process each row asynchronously
async def process_row(session, row, auth):
    key = row['key']
    issued = row['issued']
    origin = row['origin']
    
    # Define API URLs for each type of call
    urls = {
        'ACC-ACC_infra_diff_auth': f"https://api.dev.checklistbank.org/dataset/{key}/duplicate/count?authorshipDifferent=true&category=trinomial&minSize=2&mode=STRICT&status=accepted",
        'ACC-ACC_infra_eq_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?authorshipDifferent=false&category=trinomial&minSize=2&mode=STRICT&status=accepted",
        'ACC-ACC_sp_diff_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?authorshipDifferent=true&category=binomial&minSize=2&mode=STRICT&status=accepted",
        'ACC-ACC_sp_eq_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?authorshipDifferent=false&category=binomial&minSize=2&mode=STRICT&status=accepted",
        'ACC-SYN_infra_diff_acc_diff_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?acceptedDifferent=true&authorshipDifferent=true&category=trinomial&minSize=2&mode=STRICT&status=accepted&status=synonym",
        'ACC-SYN_infra_diff_acc_eq_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?acceptedDifferent=true&authorshipDifferent=false&category=trinomial&minSize=2&mode=STRICT&status=accepted&status=synonym",
        'ACC-SYN_infra_eq_acc_eq_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?acceptedDifferent=false&authorshipDifferent=false&category=trinomial&minSize=2&mode=STRICT&status=accepted&status=synonym",
        'ACC-SYN_sp_diff_acc_diff_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?acceptedDifferent=true&authorshipDifferent=true&category=binomial&minSize=2&mode=STRICT&status=accepted&status=synonym",
        'ACC-SYN_sp_diff_acc_eq_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?acceptedDifferent=true&authorshipDifferent=false&category=binomial&minSize=2&mode=STRICT&status=accepted&status=synonym",
        'ACC-SYN_sp_eq_acc_eq_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?acceptedDifferent=false&authorshipDifferent=false&category=binomial&minSize=2&mode=STRICT&status=accepted&status=synonym",
        'any_uninomial': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?category=uninomial&minSize=2&mode=STRICT&status=accepted",
        'ident_superfamily': f"https://api.checklistbank.org/dataset/{key}/duplicate?category=uninomial&limit=50&minSize=2&mode=STRICT&offset=0&rank=superfamily&status=accepted",
        'ident_family': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?category=uninomial&minSize=2&mode=STRICT&rank=family&status=accepted",
        'ident_genus': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?category=uninomial&minSize=2&mode=STRICT&rank=genus&status=accepted",
        'ident_order': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?category=uninomial&minSize=2&mode=STRICT&rank=order&status=accepted",
        'ident_subgenus': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?category=uninomial&minSize=2&mode=STRICT&rank=subgenus&status=accepted",
        'ident_tribe': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?category=uninomial&minSize=2&mode=STRICT&rank=tribe&status=accepted",
        'SYN-SYN_infra_diff_acc_diff_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?acceptedDifferent=true&authorshipDifferent=true&category=trinomial&minSize=2&mode=STRICT&status=synonym",
        'SYN-SYN_infra_diff_acc_eq_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?acceptedDifferent=true&authorshipDifferent=false&category=trinomial&minSize=2&mode=STRICT&status=synonym",
        'SYN-SYN_infra_eq_acc_diff_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?acceptedDifferent=false&authorshipDifferent=true&category=trinomial&minSize=2&mode=STRICT&status=synonym",
        'SYN-SYN_infra_eq_acc_eq_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?acceptedDifferent=false&authorshipDifferent=false&category=trinomial&minSize=2&mode=STRICT&status=synonym",
        'SYN-SYN_sp_diff_acc_diff_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?acceptedDifferent=true&authorshipDifferent=true&category=binomial&minSize=2&mode=STRICT&status=synonym",
        'SYN-SYN_sp_diff_acc_eq_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?acceptedDifferent=true&authorshipDifferent=false&category=binomial&minSize=2&mode=STRICT&status=synonym",
        'SYN-SYN_sp_eq_acc_diff_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?acceptedDifferent=false&authorshipDifferent=true&category=binomial&minSize=2&mode=STRICT&status=synonym",
        'SYN-SYN_sp_eq_acc_eq_auth': f"https://api.checklistbank.org/dataset/{key}/duplicate/count?acceptedDifferent=false&authorshipDifferent=false&category=binomial&minSize=2&mode=STRICT&status=synonym"
    }
    
    # Make asynchronous API calls for each URL
    tasks = []
    for column_name, url in urls.items():
        tasks.append(fetch(session, url, auth))
    
    # Wait for all tasks to complete
    responses = await asyncio.gather(*tasks)
    
    # Combine the responses with column names
    return {
        'key': key,
        'issued': issued,
        'origin': origin,
        **{column_name: response for column_name, response in zip(urls.keys(), responses)}
    }


async def main(releases_a, username, password):
    auth = aiohttp.BasicAuth(username, password)
    duplicates_data = []

    # Asynchronous context manager for making requests
    async with aiohttp.ClientSession() as session:
        tasks = [process_row(session, row, auth) for _, row in releases_a.iterrows()]
        duplicates_data = await asyncio.gather(*tasks)

    # Create the DataFrame 'duplicates'
    duplicates = pd.DataFrame(duplicates_data)
    return duplicates


# Example usage
if __name__ == "__main__":
    start_time = time.time()  # Measure start time
    duplicates = asyncio.run(main(releases_a, username, password))
    end_time = time.time()  # Measure end time

    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")
    print(duplicates)


#### STEP 4
# Data transposition and early warnings


## Transposition
#Select columns to be transposed
metrics_to_transpose = releases_a.columns[6:]
# Transpose the specified columns
metrics_table = releases_a[metrics_to_transpose].transpose().astype(int)
# original row indices for context
metrics_table.columns = [f'{row.alias}_{row.origin}' for i, row in releases_a.iterrows()]
# reorder columns
metrics_table=metrics_table[metrics_table.columns[::-1]]


## Early warnings
percentage_change = (metrics_table.iloc[:, -1] - metrics_table.iloc[:, -2]) / metrics_table.iloc[:, -2] * 100
metrics_table['x_change'] = metrics_table.iloc[:, -1] - metrics_table.iloc[:, -2]
metrics_table['%_change'] = percentage_change.round(2)
metrics_table['warning'] = metrics_table['%_change'].apply(lambda x: 'to_review' if abs(x) > 1 else '')




# Save dataframe
csv_file = f"metrics_{current_date}_{this_release_id}.csv"
excel_file = f"metrics_{current_date}_{this_release_id}.xlsx"
# Save duplicates DataFrame to CSV
metrics_table.to_csv(csv_file, index=True)
print(f"Metrics saved to CSV file: {csv_file}")
# Save duplicates DataFrame to Excel
metrics_table.to_excel(excel_file, index=True)
print(f"Metrics saved to Excel file: {excel_file}")


## Transposition
#Select columns with issues to be transposed
issues_to_transpose = issues.columns[:-3]
# Transpose the specified columns
issues_table = issues[issues_to_transpose].transpose()
# original row indices for context
issues_table.columns = [f'{row.alias}_{row.origin}' for i, row in issues.iterrows()]


## Early warnings
percentage_change_issues = (issues_table.iloc[:, -1] - issues_table.iloc[:, -2]) / issues_table.iloc[:, -2] * 100
issues_table['x_change'] = issues_table.iloc[:, -1] - issues_table.iloc[:, -2]
issues_table['%_change'] = percentage_change_issues.round(2)
issues_table['warning'] = issues_table['%_change'].apply(lambda x: 'to_review' if abs(x) > 10 else '')


# Save dataframe
csv_file = f"issues_{current_date}_{this_release_id}.csv"
excel_file = f"issues_{current_date}_{this_release_id}.xlsx"
# Save duplicates DataFrame to CSV
issues_table.to_csv(csv_file, index=True)
print(f"Issues saved to CSV file: {csv_file}")
# Save duplicates DataFrame to Excel
issues_table.to_excel(excel_file, index=True)
print(f"Issues saved to Excel file: {excel_file}")



## Organice and Transpose Duplicates

duplicates = duplicates.sort_values(by='issued', ascending=True)
duplicates = duplicates.sort_values(by='origin', ascending=True)
#Select columns with issues to be transposed
duplicates_to_transpose = duplicates.columns[3:]
# Transpose the specified columns
duplicates_table = duplicates[duplicates_to_transpose].transpose()
# original row indices for context
duplicates_table.columns = [f'{row.issued}_{row.origin}' for i, row in duplicates.iterrows()]
# Conver error Api messages to nan
duplicates_table = duplicates_table.apply(pd.to_numeric, errors='coerce').fillna(0)

## Early warnings Duplicates
percentage_change_duplicates = (duplicates_table.iloc[:, -1] - duplicates_table.iloc[:, -2]) / duplicates_table.iloc[:, -2] * 100
duplicates_table['x_change'] = duplicates_table.iloc[:, -1] - duplicates_table.iloc[:, -2]
duplicates_table['%_change'] = percentage_change_duplicates.round(2)
duplicates_table['warning'] = duplicates_table['%_change'].apply(lambda x: 'to_review' if abs(x) > 5 else '')



#to improbe update directory to store in the rigth place

## Save dataframe Duplicates
csv_file = f"duplicates_{current_date}_{this_release_id}.csv"
excel_file = f"duplicates_{current_date}_{this_release_id}.xlsx"
# Save duplicates DataFrame to CSV
duplicates_table.to_csv(csv_file, index=True)
print(f"Duplicate metrics saved to CSV file: {csv_file}")
# Save duplicates DataFrame to Excel
with pd.ExcelWriter(excel_file) as writer:
    duplicates_table.to_excel(writer, index=True, sheet_name='Duplicates')
print(f"Duplicate metrics saved to Excel file: {excel_file}")












