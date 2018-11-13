import tweepy
import json
import pandas as pd


# Parses the data
def parseData(fileName):
    with open(fileName) as f:
        lines = f.readlines()
    return lines

def printData(lines):
    for line in lines:
        print(line)
        
exec(open("..\config\TwitterTokens.py").read())

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True)

# create output file
outputFile = open("ffb_output.txt", "w", encoding="utf-8")

statsFile = open("..\config\week9.dat", "r", encoding="utf-8") 

# get all the users
for user in tweepy.Cursor(api.search_users, q='#fantasyfootball').items(10):
    tweets = api.user_timeline(user.id)
    # get one of the users tweets
    tweet = tweets[0]
    tweetText = tweet.text.replace('\n','')
    formatted = '{}::::{}::::{}::::{}::::{}\n'.format(user.name, user.id, tweet.created_at, tweet.retweet_count, tweetText)
    outputFile.write(formatted)

outputFile.close()

week9data = parseData("..\config\week9.dat")
printData(week9data)