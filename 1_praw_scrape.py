import pandas as pd
import praw
import json
import csv

df = pd.read_csv("post_ids.csv")
use_posts = df['id'].tolist()

# How many posts left?
print(len(use_posts))


# Read my keys
with open("keys.json") as f:
    keys = json.load(f)

# Initialize reddit API
reddit = praw.Reddit(client_id=keys['client_id'],
                     client_secret=keys['client_secret'],
                     user_agent=keys['user_agent'])

f = open('subreddit_posts_out.csv',"w") 
writer = csv.writer(f, quoting=csv.QUOTE_ALL)
header = ["id","timestamp","title","body","edited","verdict","score","num_comments"]
writer.writerow(header)

counter = 0
for idx in use_posts:

    post = reddit.submission(idx)

    score = post.score

    if score >= 3:
        title = post.title
        body = post.selftext
        edited = str(post.edited)
        num_comments = post.num_comments
        timestamp = post.created_utc
        verdict = post.link_flair_text 
        if not verdict:
            verdict =  "NA" 

        line_stuff = [idx,timestamp,title,body,edited,verdict,score,num_comments]
        writer.writerow(line_stuff)
    else:
        line_stuff = [idx,"NA","NA","NA","NA","NA",score,"NA"]
        writer.writerow(line_stuff)

    if counter % 1000 == 0:
        print(counter)
    counter += 1

f.close()

