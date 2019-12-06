import numpy as np
import pandas as pd

from NessieAPI import post_regobs
from datetime import date, timedelta, datetime


# Function generate daily 10-min means
def GenerateMeans(date, lower_bound):
    # Import data
    df = pd.read_csv('../docs/data/20191205.txt', header=None)
    df = pd.read_csv('../docs/data/{}.txt'.format(date), header=None)
    df.columns = ['date', 'level']

    # Parse date
    df['date'] = pd.to_datetime(df['date'])
    
    # Resample to desired resolution
    df.index = df['date']
    df = df.drop(columns=['date'])
    df = df.resample('10T').mean()

    # Add columns for NessieAPI and encode to JSON
    df['date'] = df.index
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['gauge_id'] = 73
    
    # Drop if already recorded
    df = df[df.date > lower_bound]

    return df


# Get last time processed
with open('ProcessNewDataLog.txt', 'r') as fo:
    last_date = fo.read()

# Get list of days that must be processed
sdate = datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S')
ndays = (datetime.now() - sdate).days + 1
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

    # Update log
    with open('ProcessNewDataLog.txt', 'w') as fo:
        newest_date = data.date.max()
        if newest_date is np.nan:
            newest_date = 0
        
        fo.write(newest_date)
