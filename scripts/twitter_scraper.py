import json

import pandas as pd
import re

from datetime import datetime, timedelta
import requests
import pandas as pd

def get_data(tweet):
    data = {
        'created_at': tweet['created_at'],
        'text': tweet['text']
    }
    return data

# we use this function to subtract 60 mins from our datetime string
def time_travel(now, mins):
    now = datetime.strptime(now, dtformat)
    back_in_time = now - timedelta(minutes=mins)
    return back_in_time.strftime(dtformat)

##########################################################
## SETUP THE API REQUEST
##########################################################
f = open("../resources/barrer-token.txt", "r")
BEARER_TOKEN = f.read()

endpoint = 'https://api.twitter.com/2/tweets/search/recent'
headers = {'authorization': f'Bearer {BEARER_TOKEN}'}
params = {
    'query': '(tesla OR tsla OR elon musk) (lang:en)',
    'max_results': '100',
    'tweet.fields': 'created_at,lang'
}

##########################################################
## SETUP THE DATES
##########################################################

dtformat = '%Y-%m-%dT%H:%M:%SZ'  # the date format string required by twitter
    
now = datetime.now()             # current date
end = now - timedelta(days=2)    # last date -> 2 days scraping data
now = now.strftime(dtformat)     # convert the current datetime to the format used for API

now = time_travel(now, 180)      # Twitter API doesn't allow to scrape real time data
                                 # so, I go 3hrs backwards

df = pd.DataFrame()              # initialize dataframe to store tweets


##########################################################
## SCRAPING LOOP
##########################################################
while True:
    
    if datetime.strptime(now, dtformat) < end:
        # if we have reached the "liimit"
        break
    
    pre60 = time_travel(now, 240)             # scrape 100 tweets every hour 
    
    params['start_time'] = pre60
    params['end_time'] = now
    
    response = requests.get(endpoint,
                            params=params,
                            headers=headers)  
    
    for tweet in response.json()['data']:

        row = get_data(tweet)  
        df = df.append(row, ignore_index=True)

    print(f"{now} - {pre60} \t Done.")

    now = pre60 


df.to_csv('../data/TSLA.csv')       # save the CSV file