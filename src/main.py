import tweepy
import json
import pandas as pd

# Converts the file to an array of lines
def getLines(fileName):
    with open(fileName) as f:
        lines = f.readlines()
    return lines

def printData(lines):
    for line in lines:
        print(line)
        
def parseData(line):
    parts = line.split("::")
    for part in parts:
        print(part)

def setupAuth():
    exec(open("..\config\TwitterTokens.py").read())
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    return tweepy.API(auth, wait_on_rate_limit = True)

def readTweets():
    # get all the users
    for user in tweepy.Cursor(api.search_users, q='#fantasyfootball').items(10):
        tweets = api.user_timeline(user.id)
        # get one of the users tweets
        tweet = tweets[0]
        tweetText = tweet.text.replace('\n','')
        formatted = '{}::::{}::::{}::::{}::::{}\n'.format(user.name, user.id, tweet.created_at, tweet.retweet_count, tweetText)
        outputFile.write(formatted)


api = setupAuth()

# create output file
outputFile = open("ffb_output.txt", "w", encoding="utf-8")
outputFile.close()

#read in the stats
statsFile = open("..\config\week9.dat", "r", encoding="utf-8") 
week9data = getLines("..\config\week9.dat")

#parse the data
for line in week9data:
    parsedLine = parseData(line)
    
#printData(week9data)
