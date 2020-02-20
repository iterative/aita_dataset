library(ggplot2)
library(dplyr)
library(lubridate)

df1 <- read.csv("subreddit_posts_a.csv")
df2 <- read.csv("subreddit_posts_b.csv")


df <- rbind(df1,df2)
df$id <- as.character(df$id)
##### Merge df3 and s 
df3 <- read.csv("../patch/subreddit_posts_text_patch.csv")
s <- read.csv("already_scraped.csv")
patch <- merge(df3,s,all.y=TRUE)
length(unique(patch$id)) == nrow(patch)


# Make the BIG ONE
big <- rbind(df,patch)
big$id <- as.character(big$id)
big <- unique(big)
# Check that every row corresponds to a unique post
length(unique(big$id)) == nrow(big)


# A sanity check
post_ids <- read.csv("post_ids.csv")
post_ids$id <- as.character(post_ids$id)
nrow(post_ids) - nrow(big)

to_scrape = setdiff(post_ids$id,big$id)

# OK THIS CHECKS OUT
thresh <- big %>%
  subset(score >= 3)

orig <- read.csv("aita_raw.csv")

difa <- setdiff(orig$id, thresh$id)
difb <- setdiff(thresh$id, orig$id)

######### Lets make a graph  ##################

# Master post id frequencies
post_ids$utc <- as.POSIXct(post_ids$timestamp, origin='1970-01-01', tz="UTC")
post_ids$utc <- as.Date(post_ids$utc)

# Summarise by month
# Make into a string?
master_count <- post_ids %>%
  group_by(month=floor_date(utc,"month"))%>%
  summarize(amount=n()) %>%
  mutate(Source = "Total number of posts")

# Version v.20.1 id counts
orig$utc <- as.Date( as.POSIXct(orig$timestamp, origin='1970-01-01', tz='UTC'))
orig_count <- orig %>%
  group_by(month=floor_date(utc,"month"))%>%
  summarize(amount=n()) %>%
  mutate(Source = "Pushshift scores ≥ 3")

# And our newest count
thresh$utc <- as.Date( as.POSIXct(thresh$timestamp, origin="1970-01-01", tz="UTC"))
new_count <- thresh %>%
  group_by(month=floor_date(utc,"month"))%>%
  summarize(amount=n()) %>%
  mutate(Source = "Praw scores ≥ 3")

counts <- rbind(master_count, orig_count, new_count)
ggplot(subset(counts, month < "2020-02-01"), aes(month,amount))+
  geom_line(aes(colour=Source),size=1)+
  ylab("# of posts")+
  theme_bw()
