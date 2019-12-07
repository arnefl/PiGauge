import numpy as np
import pandas as pd

from os.path import join
from pytz import timezone
from NessieAPI import post_regobs
from datetime import date, timedelta, datetime
from Configuration import Configuration


# Load configuration
config = Configuration()
time_zone = timezone(config['sampling']['time_zone'])


# Function generate daily means
def GenerateMeans(date, lower_bound):
    # Import data
    df = pd.read_csv(join(config['sampling']['data_folder'], 
                         '{}.txt'.format(date)), 
                     header=None)
    df.columns = ['date', 'level']

    # Parse date
    df['date'] = pd.to_datetime(df['date'])
    
    # Resample to desired resolution
    df.index = df['date']
    df = df.drop(columns=['date'])
    df = df.resample('{}T'.format(config['reporting']['resolution'])).mean()

    # Add columns for NessieAPI and encode to JSON
    df['date'] = df.index
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['gauge_id'] = config['api']['gauge_id']
    
    # Drop if already recorded
    df = df[df.date > lower_bound]

    # Drop if it's the current 10-min bin
    now = datetime.now(time_zone)
    td = timedelta(minutes = int(now.strftime('%M')[1]))
    upper_bound = (now - td).strftime('%Y-%m-%d %H:%M:00')
    df = df[df.date < upper_bound]

    return df


# Get last time processed
last_date = config['reporting']['last_report']

# Get list of days that must be processed
sdate = datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S')
ndays = (datetime.now(time_zone) - sdate).days + 1
days = [(sdate+timedelta(days=i)).strftime('%Y%m%d') for i in range(ndays)]

# For each day generate 10-min means
data = pd.DataFrame(columns=['date', 'level', 'gauge_id'])

for d in days:
    try:
        data = data.append(GenerateMeans(d, last_date), sort=False)
    except:
        continue

# If we actually have new data
if data.shape[0] > 0:
    # Post
    jsonData = data.to_json(orient='records')
    post_regobs(jsonData)

    # Update config with last reporting date
    newest_date = data.date.max()
    if isinstance(newest_date, str):
        config['reporting']['last_report'] = newest_date
        config.save()
