#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2024
@author: camisilver

Objective: Check differences between configuration and actual merged sectors
"""


import os
import requests # For API calls

import pandas as pd

import nest_asyncio
nest_asyncio.apply()
#import time
from datetime import datetime



# Set directory
os.chdir('/Users/camisilver/Documents/CatalogueOfLife/xcol/xreleases validation')
# Verify the current working directory
current_directory = os.getcwd()
print(f"Current working directory: {current_directory}")


# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")
username = 
password = 

# Get id of the latest Xrelease

#xrelease_id = 298210
xrelease_id = "3LXRC" # Use the lastest release

# Pending
# - Make api call to get merged data with bot dataset ID and subject taxa to get sector specific metrics


###### Information from sectors as configured on the project

# Extract ids from the project configuration, including priorities
url = "https://api.checklistbank.org/dataset/3/sector?datasetKey=3&limit=130&mode=merge&offset=0"

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


dataset_ids = sectors_base['dataset_id'].tolist()

# Initialize an empty list to store the data

titles = []

# Iterate over each key in the list
for dataset_id in dataset_ids:
    # Construct the URL for the API call
    url = f"https://api.checklistbank.org/dataset/{dataset_id}"
    
    try:
        # Fetching the JSON data from the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        json_data = response.json()
        
        # Extracting the title from the JSON data
        title = json_data.get('title', 'No Title Found')  # Default to 'No Title Found' if title is missing
        
        # Append the key and title to the data list
        titles.append({'dataset_id': dataset_id, 'title': title})
    
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        print(f"Error fetching data for key {dataset_id}: {e}")
        titles.append({'dataset_id': dataset_id, 'title': 'Error fetching title'})

titles = pd.DataFrame(titles)


sectors_base = pd.merge(sectors_base,titles, on='dataset_id', how='left')
sectors_base = sectors_base.drop_duplicates()


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
#dataset_nameCount['dataset_id'] = dataset_nameCount['dataset_id'].apply(lambda x: str(int(x)) if x.is_integer() else str(x))


###### Information from merged sectors

# To improve
# datasetKey as a preset variable


#url = "https://api.checklistbank.org/dataset/295850/sector?datasetKey=295850&limit=100&mode=merge&offset=0"
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/sector?datasetKey={xrelease_id}&limit=130&mode=merge&offset=0"

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

# Make the API calls for each row in dataset_nameCount
for index, row in dataset_nameCount.iterrows():
    try:
        dataset_id = int(float(row['dataset_id']))  # Ensure dataset_id is an integer
        url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?&sectorDatasetKey={dataset_id}&sectorMode=merge"
        response = requests.get(url, auth=(username, password))   
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Extract the "total" value 
            total_value = data.get('total', None)
            
            # Store the value in the 'merged_names' column
            dataset_nameCount.loc[index, 'merged_names'] = total_value
        else:
            # Provide more detailed error information
            print(f"Failed to retrieve data for dataset_id={dataset_id}: Status Code: {response.status_code}, Response: {response.text}")
    except ValueError as e:
        print(f"Error converting dataset_id for row {index}: {e}")


#merged_df['dataset_id'] = merged_df['dataset_id'].apply(lambda x: str(int(x)) if x.is_integer() else str(x))
dataset_nameCount['dataset_id'] = dataset_nameCount['dataset_id'].astype('int64')
merged_df['dataset_id'] = merged_df['dataset_id'].astype('int64')
result = pd.merge(merged_df, dataset_nameCount, on='dataset_id', how='left').drop_duplicates()
result = result.dropna(subset=['priority'])

# Dynamic filename for export
this_release_id = int(result['release_id'].iat[0])

output_name = f'sources_{current_date}_{this_release_id}.csv'
result.to_csv(output_name, index=False)

#-----

#response = requests.get('https://api.checklistbank.org/dataset/1008', headers={'Accept': 'application/json'})
#data = response.json()
#print(data)

