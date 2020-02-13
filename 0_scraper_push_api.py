# We go through the push API to get the ids of every post, then use the official reddit
# API to get the contents of each post and metadata of interest.
import requests
import json
import pandas as pd
import time

first_epoch = 1577836800  # Jan 1, 2020
last_epoch = 1580515200 # Feb 1, 2020

def getPushshiftData(after, before):
    url = 'https://api.pushshift.io/reddit/submission/search/?sort_type=created_utc&sort=asc&subreddit=amitheasshole&after='+ str(after) +"&before"+str(before)+"&size=1000"
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

timestamps = list()
post_ids = list()
score = list()

after = first_epoch
while int(after) < last_epoch:
    data = getPushshiftData(after,last_epoch)
    for post in data:
        tmp_time = post['created_utc']
        tmp_id = post['id']
        tmp_score = post['score']
        timestamps.append(tmp_time)
        post_ids.append(tmp_id)
        score.append(tmp_score)
    after = timestamps[-1]
    print([str(len(post_ids)) + " posts collected so far."])
    time.sleep(0.1)

# Write to a csv file
d = {'id':post_ids, 'timestamp':timestamps, 'score':score}
df = pd.DataFrame(d)
df.to_csv("posts_ids_and_scores_0120.csv", index=False)