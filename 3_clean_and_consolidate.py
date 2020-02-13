# Do some cleaning to get the data in good order for a classification problem

import pandas as pd

def clean_scrape(df):
    # Make verdicts all lower case
    df['verdict'] = df['verdict'].str.lower()
    # Replace some common alternate spellings
    df['verdict'] = df['verdict'].str.replace("a--hole|a-hole","asshole") 
    # Just keep answers with standard verdicts
    valid_list = ["asshole","not the asshole","everyone sucks","no assholes here"]
    df_use = df[df['verdict'].isin(valid_list)]
    # Remove any edits that may give away the answer [ie, "edit: okay you're right I'm the asshole" ]
    df_use['body'] = df_use['body'].str.replace("(edit|update).*?(YTA|a-|ass|\\sta\\s)(.*)","",case=False)
    # Remove any deleted or removed posts
    gone_list = ["[deleted]","[removed]",""]
    df_use = df_use[df_use['body'].isin(gone_list)==False]
    print("After removing deleted posts, there are " +  str(len(df_use)) + " posts left.")
    # Make a grand binary variable conslidating "no assholes here" and "everyone sucks" into the dominant classes
    df_use["is_asshole"] = [1 if x in ["asshole","everyone sucks"] else 0 for x in df_use["verdict"]]
#to keep 8
    # Write to file
    #df_use.to_csv("AITA_cleaned.csv")
    return(df_use)


def merge_scrape(old, new):
    # old and new are pandas dataframes. should have the same columns
    old = pd.concat([old,new])
    old = old.drop_duplicates()
    return(old)

raw = pd.read_csv("subreddit_scrape_0120.csv")
new = clean_scrape(raw)
old = pd.read_csv("AITA_clean.csv")
grand = merge_scrape(old,new)

print("There are now " +  str(len(grand)) + " posts.")

grand.to_csv("AITA_clean.csv",index=False)