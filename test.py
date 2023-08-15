# play ground the main file is main.py
#THIS IS PLAYGROUND


import pandas as pd
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


# Connect to the PostgreSQL engine
eng = create_engine('postgresql://readonly:3535Harbor@geodbinstance.cottkh4djef2.us-west-2.rds.amazonaws.com/empa2021')

# Define system fields
SYSTEM_FIELD = [
    # system field names...
]

# URL of the schema page
url = "https://empachecker.sccwrp.org/checker/schema"

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content of the page with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the links on the page
links = soup.find_all('a')

# Initialize an empty dictionary to hold the data types and table names
dtypes = {}

# Iterate over the links
for link in links:
    # The href attribute of the link should be the data type
    datatype = link.get('href')
    
    # If the datatype exists and it's not the main page or Excel download
    if datatype and 'main' not in datatype and 'xlsx' not in datatype:
        # Send a GET request to the data type page
        response = requests.get(url + '/' + datatype)
        
        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all the table names on the page
        tables = soup.find_all('strong')
        
        # Store the table names in the dtypes dictionary
        dtypes[datatype] = [table.text for table in tables]

# Print the dtypes dictionary to check the result
print(dtypes)
