#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2024
@author: camisilver

Objective: Check differences between configuration and actual merged sectors
"""


import requests # For API calls
#from requests.auth import HTTPBasicAuth # For API calls that need authentication
#import xml.etree.ElementTree as ET

import pandas as pd
# pip install aiohttp
#import aiohttp 
#import asyncio #To improve API performance, asyncronus calls
#pip install nest_asyncio
import nest_asyncio
nest_asyncio.apply()
#import time
from datetime import datetime


# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")


# Get id of the latest Xrelease

xrelease_id = 298210


# Pending
# - Extract via API the id of latest xrelease
# - Replace from url xrelease id so it is stablished before hand
# - Add name of dataset
# - Make api call to get merged data with bot dataset ID and subject taxa to get sector specific metrics


###### Information from sectors as configured on the project

# Extract ids from the project configuration, including priorities
url = "https://api.checklistbank.org/dataset/3/sector?datasetKey=3&limit=100&mode=merge&offset=0"

response = requests.get(url, auth=(username, password))
if response.status_code == 200: # successful ?
    data = response.json()     # Parse JSON
    
    # Extract and print the "total" number of sectors added to the project to compare later with the merged ones
    total_value = data.get('total')
    print(f"Total: {total_value}")
    
    # Extract required fields from the parsed JSON results
    extracted_data = []
    for result in data['result']:
        extracted_data.append({
            "sector_id": result.get("id"),
            "dataset_id": result.get("subjectDatasetKey"),
            "priority": result.get("priority"),
            "created": result.get("created")[:10],  # Keep only yyyy-mm-dd
            "modified": result.get("modified")[:10]  # Keep only yyyy-mm-dd
        })
    # new dataframe
    sectors_base = pd.DataFrame(extracted_data)
    # print(sectors_base.head())  
    print("Failed to retrieve data. Status code:", response.status_code)


# Extract information from each dataset that is use for the xrelease
# uses the setor_base dataframe created on the previous step

base_url = 'http://api.checklistbank.org/dataset/'

def make_api_call(dataset_id):
    url = f"{base_url}{dataset_id}/import?state=finished"

    response = requests.get(url, auth=(username, password))
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.status_code}

# Dictionary to store responses
dict_sourceDatasets = {}

# Iterate over each dataset_id in the DataFrame
for dataset_id in sectors_base['dataset_id']:
    dict_sourceDatasets[dataset_id] = make_api_call(dataset_id)


dataset_keys = []
name_counts = []

# Iterate over each item in the dictionary
for dataset_id, response_list in dict_sourceDatasets.items():
    if isinstance(response_list, list) and len(response_list) > 0:
        # Extract datasetKey and nameCount from the first item in the list
        response = response_list[0]
        dataset_keys.append(response.get('datasetKey'))
        name_counts.append(response.get('nameCount'))
    else:
        # Just in case If there's an error or empty response
        dataset_keys.append(None)
        name_counts.append(None)

# Create a DataFrame using the lists
dataset_nameCount = pd.DataFrame({
    'dataset_id': dataset_keys,
    'total_nameCount': name_counts
})


dataset_nameCount.dropna(axis=0, how='all', inplace=True)
dataset_nameCount['dataset_id'] = dataset_nameCount['dataset_id'].apply(lambda x: str(int(x)) if x.is_integer() else str(x))


###### Information from merged sectors

# To improve
# datasetKey as a preset variable


#url = "https://api.checklistbank.org/dataset/295850/sector?datasetKey=295850&limit=100&mode=merge&offset=0"
url = "https://api.checklistbank.org/dataset/298210/sector?datasetKey=298210&limit=100&mode=merge&offset=0"

response = requests.get(url, auth=(username, password))

# Check if the request was successful
if response.status_code == 200:

    data = response.json()     # Parse JSON
    # Extract and print the "total" value of sectors that where merged on the xrelease
    total_value = data.get('total')
    print(f"Total: {total_value}")
    
    results_list = data.get('result', [])
    sectors_dict = pd.json_normalize(results_list).to_dict(orient='records')
    # Create a dataframe
    merged_sectors = []
    for sector in results_list:
        sector_dict = {
            'sector_id': sector.get('id'),
            'dataset_id': sector.get('subjectDatasetKey'),
            'release_id': sector.get('datasetKey'),
            'target': sector.get('target', {}).get('name'),
            'subject': sector.get('subject', {}).get('name')
        }
        merged_sectors.append(sector_dict)
    
    # Create DataFrame
    merged_sectors = pd.DataFrame(merged_sectors)
    
else:
    print(f"Failed to retrieve data: {response.status_code}")


#put together sectors configuresd and actuall sectors being merged
merged_df = pd.merge(sectors_base, merged_sectors, on=['dataset_id', 'sector_id'], how='outer')
    
    
# Names merged by each dataset that has at least one sector on the project
# This does not diferentiate by sector

#url_template = "https://api.checklistbank.org/dataset/295850/nameusage/search?limit=1&offset=0&sectorDatasetKey={dataset_id}&sectorMode=merge"
url_template = "https://api.checklistbank.org/dataset/298210/nameusage/search?limit=1&offset=0&sectorDatasetKey={dataset_id}&sectorMode=merge"

# Make the API calls for each row in dataset_nameCount
for index, row in dataset_nameCount.iterrows():
    url = url_template.format(dataset_id=row['dataset_id'])
    response = requests.get(url, auth=(username, password))   
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract the "total" value 
        total_value = data.get('total', None)
        
        # Store the  in the 'names' column
        dataset_nameCount.loc[index, 'merged_names'] = total_value
    else:
        # Provide more detailed error information
        print(f"Failed to retrieve data for dataset_id={row['dataset_id']}: Status Code: {response.status_code}, Response: {response.text}")


#merged_df['dataset_id'] = merged_df['dataset_id'].apply(lambda x: str(int(x)) if x.is_integer() else str(x))
dataset_nameCount['dataset_id'] = dataset_nameCount['dataset_id'].astype('int64')
merged_df['dataset_id'] = merged_df['dataset_id'].astype('int64')
result = pd.merge(merged_df, dataset_nameCount, on='dataset_id', how='left')

# Dynamic filename for export
output_name = f'sources_{current_date}_{xrelease_id}.csv'
result.to_csv(output_name, index=False)

#-----

#response = requests.get('https://api.checklistbank.org/dataset/1008', headers={'Accept': 'application/json'})
#data = response.json()
#print(data)
