#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 13:42:17 2025

@author: camisilver
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from datetime import datetime
import asyncio
import aiohttp
import time


# Set directory
os.chdir('/Users/camisilver/Documents/CatalogueOfLife/xcol/xreleases validation')
# Verify the current working directory
current_directory = os.getcwd()
print(f"Current working directory: {current_directory}")

current_date = datetime.now().strftime("%Y-%m-%d")


#Authentication
username = 
password = 

# Define the release that will be analyzed
#xrelease_id = 300043 # Define specific release id 3LXRC
xrelease_id = "3LXRC" # Use the lastest release



# API endpoint and parameters
#url = "https://api.checklistbank.org/dataset/3/sector" # All datasets on project
url = "https://api.checklistbank.org/dataset/3LXRC/sector"  # All datasets added to the last release
params = {
    #"datasetKey": "3", use it when running for the entiry project
    "limit": 800,
    "offset": 0,
    "publisherKey": "750a8724-fa66-4c27-b645-bd58ac5ee010"
}


# Extract list of BDJ datasets added to the COL project, and extract some metadata
response = requests.get(url, params=params, auth=(username, password))

# Check for a successful response
if response.status_code == 200:
    # Store the response JSON in BDJ_dict
    BDJ_dict = response.json()

    # Extract the relevant fields and create a DataFrame
    if "result" in BDJ_dict:
        data = BDJ_dict["result"]
        BDJ_df = pd.DataFrame(data)[["id", "subjectDatasetKey", "size", "created"]]
        print("DataFrame created successfully:")
        print(BDJ_df.head())

        # Create BDJ_metrics by making API calls for each subjectDatasetKey
        BDJ_metrics = {}
        for key in BDJ_df["subjectDatasetKey"]:
            metrics_url = f"https://api.checklistbank.org/dataset/{key}/import?state=finished"
            metrics_response = requests.get(metrics_url, auth=(username, password))

            if metrics_response.status_code == 200:
                BDJ_metrics[key] = metrics_response.json()
            else:
                BDJ_metrics[key] = {"error": f"Failed to fetch data: {metrics_response.status_code}"}

        print("BDJ_metrics created successfully:")

    else:
        print("Key 'result' not found in the API response.")
else:
    print(f"Failed to fetch data: {response.status_code} - {response.text}")


BDJ_df.rename(columns={'subjectDatasetKey': 'key'}, inplace=True)


# Extract metadata using the dataset key
BDJ_metadata_dict = {}

# Base API URL
base_url = "https://api.checklistbank.org/dataset/"

# Iterate through the 'subjectDatasetKey' column
for key in BDJ_df['key']:
    try:
        # Make the API call
        response = requests.get(f"{base_url}{key}")
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        
        # Store the JSON response in the dictionary
        BDJ_metadata_dict[key] = response.json()
        
    except requests.exceptions.RequestException as e:
        # Handle exceptions (e.g., network errors, invalid keys)
        print(f"Error with key {key}: {e}")


# Optionally, save the dictionary to a file for later use
import json
with open('BDJ_metadata.json', 'w') as f:
    json.dump(BDJ_metadata_dict, f, indent=4)


# Create a new DataFrame to store the extracted metadata
BDJ_metadata_df = pd.DataFrame(columns=['version', 'title', 'size-org'])

# Iterate over the dictionary to extract the version and title
for key, metadata in BDJ_metadata_dict.items():
    # Safely extract the values, using `.get()` to avoid KeyError
    version = metadata.get('version', None)
    title = metadata.get('title', None)
    size = metadata.get('size', None)
    
    # Append the data as a new row in the DataFrame
    BDJ_metadata_df = pd.concat([
        BDJ_metadata_df,
        pd.DataFrame({'key': [key], 'version': [version], 'title': [title], 'size-org': [size] })
    ], ignore_index=True)


BDJ_df = pd.merge(BDJ_df, BDJ_metadata_df, on='key', how='inner')


# Iterate over items in metrics_dict to extract issues
issues_bdj = pd.DataFrame(columns=['key', 'Issue Type', 'Count'])

# Iterate over items in metrics_dict
for key, value_list in BDJ_metrics.items():
    # Check if value is a list and not empty
    if isinstance(value_list, list) and value_list:
        # Assuming you want the first item in the list
        value_dict = value_list[0]
        # Check if value_dict is a dictionary and contains 'issuesCount'
        if isinstance(value_dict, dict) and 'issuesCount' in value_dict:
            issues_count_dict = value_dict['issuesCount']
            
            # Append data to the DataFrame
            for issue_type, count in issues_count_dict.items():
                issues_bdj = pd.concat([issues_bdj, pd.DataFrame([{'key': key, 'Issue Type': issue_type, 'Count': count}])], ignore_index=True)
        else:
            print(f"No issue count data found for key: {key}")
    else:
        print(f"No data found or empty list for key: {key}")
        
issues_bdj = issues_bdj.pivot_table(index='key', columns='Issue Type', values='Count', fill_value=0)
issues_bdj.reset_index(inplace=True) # Reset the index

 # Count how many columns are different from zero for each row
issues_bdj['non_zero_count'] = issues_bdj.apply(lambda row: (row != 0).sum(), axis=1)
issues_bdj = pd.merge(BDJ_df, issues_bdj, on='key', how='inner')



report_name= f'BDJ_issuesMerged_{current_date}.csv'
issues_bdj.to_csv(report_name,index=True)





