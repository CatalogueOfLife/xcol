#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 14:21:46 2024

@author: camisilver
"""

import os
import requests # For API calls
from requests.auth import HTTPBasicAuth # For API calls that need authentication
import pandas as pd
from datetime import datetime


# Set directory
os.chdir('/Users/camisilver/Documents/CatalogueOfLife/xcol/xreleases validation')
# Verify the current working directory
current_directory = os.getcwd()
print(f"Current working directory: {current_directory}")

# Get the current date in YYYY-MM-DD format
current_date = datetime.now().strftime("%Y-%m-%d")



# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")
username = 
password = 
#username = 
#password = 


# API URL
#key = "3LR" # normal release
key = "3LXRC" #extended release
api_url = f"https://api.checklistbank.org/dataset/{key}/import?state=finished"



result_list = []

response = requests.get(api_url, auth=HTTPBasicAuth(username, password))

if response.status_code == 200:
    # Store the result in a list
    result_list = response.json()
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")


# Initialize lists to store the data for each DataFrame
names_by_rank_data = []
taxa_by_rank_data = []
usages_by_status_data = []

# Iterate on result_list to extract data from  sub-dictionary
for item in result_list:
    key = item.get('key')  # Assuming 'key' is a field in your data
    
    # Extract and store "namesByRankCount" data
    names_by_rank_count = item.get('namesByRankCount', {})
    for rank, count in names_by_rank_count.items():
        names_by_rank_data.append({ 'rank': rank, 'count': count})
    
    #Extract and store "taxaByRankCount" data
    taxa_by_rank_count = item.get('taxaByRankCount', {})
    for rank, count in taxa_by_rank_count.items():
        taxa_by_rank_data.append({ 'rank': rank, 'count': count})
    
    # STEP 2.5: Extract and store "usagesByStatusCount" data
    usages_by_status_count = item.get('usagesByStatusCount', {})
    for status, count in usages_by_status_count.items():
        usages_by_status_data.append({'status': status, 'count': count})

# Convert the lists into DataFrames
names_by_rank = pd.DataFrame(names_by_rank_data)
taxa_by_rank = pd.DataFrame(taxa_by_rank_data)
usages_by_status = pd.DataFrame(usages_by_status_data)


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
#this_release_id = "307486"


names_by_rank.to_excel(f"names_by_rank_{current_date}_{this_release_id}.xlsx", index=False)
taxa_by_rank.to_excel(f"taxa_by_rank_{current_date}_{this_release_id}.xlsx", index=False)
usages_by_status.to_excel(f"usages_by_status_{current_date}_{this_release_id}.xlsx", index=False)




