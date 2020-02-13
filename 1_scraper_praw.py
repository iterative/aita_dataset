import praw
import pandas as pd
import csv
import json

# Read in the list of post ids
df = pd.read_csv("post_ids_and_scores_0120.csv")
# Filter only posts with 3+ upvotes
df_use = df[df['score'] >= 3]
use_posts = df_use['id'].tolist()
use_score = df_use['score'].tolist()
use_timestamp = df_use['timestamp'].to_list()

print(len(df_use))
# Read my keys
with open("keys.json") as f:
    keys = json.load(f)

# Initialize reddit API
reddit = praw.Reddit(client_id=keys['client_id'],
                     client_secret=keys['client_secret'],
                     user_agent=keys['user_agent'])

# For each post in the list, get the data we care about
f = open('subreddit_scrape.csv',"w") 
writer = csv.writer(f, quoting=csv.QUOTE_ALL)
header = ["id","timestamp","title","body","edited","verdict","score","num_comments"]
writer.writerow(header)

counter = 0
for idx in use_posts:

    timestamp = use_timestamp[counter]
    score = use_score[counter]

    post = reddit.submission(idx)
    title = post.title
    body = post.selftext
    edited = str(post.edited)
    num_comments = post.num_comments
    verdict = post.link_flair_text 
    if not verdict:
        verdict =  "NA" 

    line_stuff = [idx,timestamp,title,body,edited,verdict,score,num_comments]
    writer.writerow(line_stuff)

    if counter % 1000 == 0:
        print(counter)
    counter += 1

f.close()

