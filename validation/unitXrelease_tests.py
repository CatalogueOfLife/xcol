#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:54:52 2024
Update 2025-02-06

@author: camisilver
"""

import os
import pandas as pd
import numpy as np
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth

# Set directory
os.chdir('/Users/camisilver/Documents/CatalogueOfLife/xcol/xreleases validation')
# Verify the current working directory
current_directory = os.getcwd()
print(f"Current working directory: {current_directory}")

# Get the current date in YYYY-MM-DD format
current_date = datetime.now().strftime("%Y-%m-%d")

# Username and password for authentication
username = 
password = 

# Define the release that will be analyzed
# xrelease_id = # Define specific release id
xrelease_id = "3LXRC" # Use the lastest release


#Create tests dataframe
test_df = pd.DataFrame(columns=['issue', 'test_result', 'url_issue', 'clb_url'])

# Function to concat new values to the DataFrame
def add_values_to_df(test_df, issue, test_result, url_issue, clb_url):
    new_row = pd.DataFrame([{
        'issue': issue, 
        'test_result': test_result, 
        'url_issue': url_issue, 
        'clb_url': clb_url
    }])
    test_df = pd.concat([test_df, new_row], ignore_index=True)
    return test_df


###  Unit test 'issue_'

#------


###  Unit test 'issue_582'

unit_test= 'issue_582'
issue_url= 'https://github.com/gbif/backbone-feedback/issues/582'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Eucolliuris oliveri&status=accepted&type=EXACT'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Eucolliuris oliveri&status=accepted&type=EXACT"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total == 0:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)

#------



###  Unit test 'issue_882_2'

unit_test= 'issue_882_2'
issue_url= 'https://github.com/CatalogueOfLife/data/issues/882'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?SECTOR_DATASET_KEY=2144&q=Achnanthes peragalli&status=accepted&type=EXACT'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?SECTOR_DATASET_KEY=2144&q=Achnanthes peragalli&status=accepted&type=EXACT"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)

#------


###  Unit test 'issue_882_1'

unit_test= 'issue_882_1'
issue_url= 'https://github.com/CatalogueOfLife/data/issues/882'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?SECTOR_DATASET_KEY=2144&q=Achnanthes clevei&status=accepted&type=EXACT'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?SECTOR_DATASET_KEY=2144&q=Achnanthes clevei&status=accepted&type=EXACT"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)



#------


###  Unit test 'issue_574'
unit_test= 'issue_574'
issue_url= 'https://github.com/CatalogueOfLife/data/issues/574'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Corthylio calendula&sortBy=taxonomic&type=EXACT'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Corthylio calendula&sortBy=taxonomic&type=EXACT"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)


#------

###  Unit test 'issue_362'
unit_test= 'issue_362'
issue_url= 'https://github.com/CatalogueOfLife/data/issues/362'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Fenusa ewaldi&sortBy=taxonomic&type=EXACT'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Fenusa ewaldi&sortBy=taxonomic&type=EXACT"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)


#------

###  Unit test 'issue_73_author'
unit_test= 'issue_145_BBG'
issue_url= 'https://github.com/gbif/backbone-feedback/issues/145'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Myzinum&sortBy=taxonomic&type=EXACT&sectorMode=merge'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Abronia mellifera&sortBy=taxonomic&type=EXACT&sectorMode=merge"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)


###  Unit test 'issue_73_author'
unit_test= 'issue_73_author'
issue_url= 'https://github.com/CatalogueOfLife/xcol/issues/73'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Abronia mellifera&sortBy=taxonomic&type=EXACT&sectorMode=merge'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Abronia mellifera&sortBy=taxonomic&type=EXACT&sectorMode=merge"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)

#------

###  Unit test 'issue_73_source'
unit_test= 'issue_73_source'
issue_url= 'https://github.com/CatalogueOfLife/xcol/issues/73'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Abronia moreletii&sortBy=taxonomic&type=EXACT&sectorMode=merge'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Abronia moreletii&sortBy=taxonomic&type=EXACT&sectorMode=merge"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)

#------

###  Unit test 'issue_73'
unit_test= 'issue_73_year'
issue_url= 'https://github.com/CatalogueOfLife/xcol/issues/73'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Abapeba grassima&sortBy=taxonomic&type=EXACT&sectorMode=merge'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Abapeba grassima&sortBy=taxonomic&type=EXACT&sectorMode=merge"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)

#------


###  Unit test 'issue_70'
unit_test= 'issue_70'
issue_url= 'https://github.com/CatalogueOfLife/xcol/issues/70'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Aspidosiphon quadratoides&sortBy=taxonomic&type=EXACT&sectorMode=merge'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Aspidosiphon quadratoides&sortBy=taxonomic&type=EXACT&sectorMode=merge"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)

#------

###  Unit test 'issue_111'
unit_test= 'issue_111'
issue_url= 'https://github.com/CatalogueOfLife/xcol/issues/111'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Protoperidinium&sortBy=taxonomic&type=EXACT&sectorMode=merge'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Protoperidinium&sortBy=taxonomic&type=EXACT&sectorMode=merge"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)

#------


###  Unit test 'issue_131'
unit_test= 'issue_131_Hemiloricaria'
issue_url= 'https://github.com/CatalogueOfLife/xcol/issues/131'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Hemiloricaria&sortBy=taxonomic&type=EXACT&sectorMode=merge'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Hemiloricaria&sortBy=taxonomic&type=EXACT&sectorMode=merge"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)

#------

###  Unit test 'issue_146_1'
unit_test= 'issue_146_1'
issue_url= 'https://github.com/CatalogueOfLife/xcol/issues/146'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Ancistrocoma&rank=genus&sortBy=taxonomic&status=accepted'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Ancistrocoma&rank=genus&sortBy=taxonomic&status=accepted"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")
    
    
test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)
#------


###  Unit test 'issue_146_2'
unit_test= 'issue_146_2'
issue_url= 'https://github.com/CatalogueOfLife/xcol/issues/146'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Hypocomella&rank=genus&sortBy=taxonomic&status=accepted'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Hypocomella&rank=genus&sortBy=taxonomic&status=accepted"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")
    
test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)

#------

###  Unit test 'issue_146_3'
unit_test= 'issue_146_Acrochaetium'
issue_url= 'https://github.com/CatalogueOfLife/xcol/issues/146'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Acrochaetium&rank=genus&sortBy=taxonomic&status=accepted'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Acrochaetium&rank=genus&sortBy=taxonomic&status=accepted"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")
    
test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)

#------

###  Unit test 'issue_146_4'
unit_test= 'issue_146_Acanthosiphonia'
issue_url= 'https://github.com/CatalogueOfLife/xcol/issues/146'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Acanthosiphonia&rank=genus&sortBy=taxonomic&status=accepted'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Acanthosiphonia&rank=genus&sortBy=taxonomic&status=accepted"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")
    
test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)

#------


###  Unit test 'issue_113'

unit_test= 'issue_113'
issue_url= 'https://github.com/CatalogueOfLife/xcol/issues/113'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Abbella%20zabinskii&sortBy=taxonomic&type=EXACT'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Abbella%20zabinskii&sortBy=taxonomic&type=EXACT"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)

#------




###  Unit test 'issue_106'
unit_test= 'issue_106'
issue_url= 'https://github.com/CatalogueOfLife/xcol/issues/106'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=carolia couchii'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=carolia couchii"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
results = data.get('result', [])
usage_list = [result.get('usage', {}) for result in results if isinstance(result, dict)]
label_list = [usage_list.get('link', {}) for usage_list in usage_list if isinstance(usage_list, dict)]

def check_labels(labels):
    for label in labels:
        if "marinespecies" not in label:
            return "failed"
    return "succeded"

result = check_labels(label_list)
print(f"Test {unit_test} {result}, original issue: {issue_url}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)
#------


###  Unit test 'issue_109'
unit_test= 'issue_109'
issue_url= 'https://github.com/CatalogueOfLife/xcol/issues/109'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?q=Aciculidae&sortBy=taxonomic&type=EXACT'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?q=Aciculidae&sortBy=taxonomic&type=EXACT"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
total = data.get('total', 'Total not found')
# Printing the appropriate message based on the value of total
if isinstance(total, int):
    if total > 1:
        result= 'failed'
        print(f"Test {unit_test} failed, original issue: {issue_url}")
    else:
        result= 'succeded'
        print(f"Test {unit_test} succeeded, original issue: {issue_url}")
else:
    print(f"Test {unit_test} failed: {total}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)
#------

###  Unit test 'issue_79'
unit_test= 'issue_79'
issue_url= 'https://github.com/CatalogueOfLife/xcol/issues/79'
clb_url= f'https://www.checklistbank.org/dataset/{xrelease_id}/names?extinct=1&sectorMode=merge&sortBy=taxonomic'
# URL for the API call
url = f"https://api.checklistbank.org/dataset/{xrelease_id}/nameusage/search?extinct=1&sectorMode=merge&limit=10&offset=5"
# Making the API call with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))
data = response.json()
results = data.get('result', [])
# Extract 'usage' subdictionary for each item in the results list list comprehension to extract the usage subdictionary from each dictionary
usage_list = [result.get('usage', {}) for result in results if isinstance(result, dict)]
label_list = [usage_list.get('label', {}) for usage_list in usage_list if isinstance(usage_list, dict)]

def check_labels(labels):
    for label in labels:
        if not label.startswith("†"):
            return "failed"
    return "succeded"

result = check_labels(label_list)
print(f"Test {unit_test} {result}, original issue: {issue_url}")

test_df = add_values_to_df(test_df, unit_test, result, issue_url, clb_url)


this_release_id= "307161"

test_df.to_excel(f"UnitTests_{current_date}_{this_release_id}.xlsx", index=False)

#------


###  Unit test 'issue_'

#------


###  Unit test 'issue_'

#------

   




    