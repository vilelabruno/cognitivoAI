import pandas as pd

df = pd.read_csv('../input/AppleStore.csv')

#cat news and max rating count tot

outDf = df[df['rating_count_tot'] == df['rating_count_tot'][df['prime_genre'] == "News"].max()]

outDf = pd.concat([outDf, df[(df['prime_genre'] == "Book") | (df['prime_genre'] == "Music")].sort_values("rating_count_tot", ascending=False).iloc[:10]], ignore_index=True  )

from twython import Twython
import json
from datetime import datetime
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)
    
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

def diff_dates(date1, date2):
    return abs(date2-date1).minute

def tt_to_date(dt):
    dt = datetime.strptime(dt[4:19]+dt[26:], "%b %d %H:%M:%S%Y")
    return dt

for mb in outDf['track_name'].iloc[1:]:
    query = {'q': mb,
                'result_type': 'popular',
                'count': 100,
                'lang': 'pt',
                }
    print(mb)
    searchPage = python_tweets.search(**query)['statuses']
    print(searchPage)
    count = 0
    now = datetime.now()
    flag = True
    while (len(searchPage) != 0) and (flag): 
        searchPage = python_tweets.search(**query, max_id=searchPage[len(searchPage)-1]['id']-1)['statuses']
        
        for status in searchPage:
            count = count + 1
            tt_date = tt_to_date(status['created_at'])
            lastMinutes = 5
            print(diff_dates(now, tt_date))
            if diff_dates(now, tt_date) > lastMinutes:
                flag = False
                break

    outDf['n_citacoes'] = count

columns = ['id', 'track_name', 'n_citacoes', 'size_bytes', 'price', 'prime_genre']

for i in outDf.columns:
    if i not in columns:
        del outDf[i]

outDf.to_csv('../output/out.csv', index=False)
outDf.to_json('../output/out.json')