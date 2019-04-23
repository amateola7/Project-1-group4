import pandas as pd
import numpy as np
import datetime
import requests
import json
now = datetime.datetime.now()

def get_data(indicator='SP.POP.TOTL',date=now.year,country='all'):
    '''
    Retrieves data from the World Bank OpenData site.
    indicator=''
    date=''
    country=''
    
    '''
    # basic url for requesting country data.  By default pulls fifty items per request (one page).
    baseURL = "https://api.worldbank.org/v2/country/{0}/indicator/{1}?date={2}&format=json"
    # Pull data for a given indicator, country (or 'all'), and year/years (ex. 1980, 1980:1990)
    results = requests.get(baseURL.format(country,indicator,date)).json()
    # Find the number of pages in this request pull
    number_of_pages = results[0]['pages']
    # Save the first page in a list
    data_returned = [results[1]]
    # Pull the rest of the pages
    for page in range(2,number_of_pages+1):
        baseURL = "https://api.worldbank.org/v2/country/{0}/indicator/{1}?date={2}&page={3}&format=json"
        results = requests.get(baseURL.format(country,indicator,date,page)).json()
        data_returned.append(results[1])
    # Create a simple dataframe for the data.   
    df = pd.DataFrame(columns=['ISO','Year',indicator])
    # Load the data into the dataframe
    for pg in data_returned:
        for obs in pg:
            try:
                # Skip the region and world data by only pulling data associated with a country code.  
                if obs['countryiso3code'] == '':
                    next
                else:
                    df.loc[df.shape[0]]=[obs['countryiso3code'],obs['date'],obs['value']]
            except:
                next
    # return a pandas dataframe            
    return df
