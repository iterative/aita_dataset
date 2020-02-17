# AITA_Dataset

This repo contains code to replicate our scrape of the r/AmItheAsshole subreddit, as well as .dvc files linking this GitHub repo to an S3 bucket hosting the dataset. 

Building the dataset is accomplished in three scripts:
1. `0_scraper_push_api.py` collects Reddit post ids and scores from within a desired timeframe.
2. `1_scraper_praw.py` uses the praw library to query each post by id, and grab associated text and meta-data.
3. `2_clean_and_consolidate.py` cleans data and does some general neatening. 

The dataset contained in `aita_clean.csv` has 9 features:

-id, a unique string provided by Reddit's API to index every post
-timestamp of post creation, in epoch/Unix format
-title, a string t
-body, a string 
-edited, the timestamp at which a post was edited. If no edits occurred this field is False.
-verdict, a string in the set {"asshole", "not the asshole", "everyone sucks", "no assholes here") 
-score, an integer corresponding to the difference between upvotes and downvotes
-num_comments, an integer corresponding to the total number of comments (including nested discussion) to the post
-is_asshole, a boolean corresponding to whether the verdict is in the set {"asshole","everyone sucks"}

To get this dataset, install DVC and run:

`$ dvc get https://github.com/iterative/aita_dataset aita_clean.csv`

or

`$ dvc import https://github.com/iterative/aita_dataset aita_clean.csv` to also download the associated .dvc files for data set versioning. 
