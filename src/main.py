import tweepy
import json
import pandas as pd
import player as player
import game as game

# Converts the file to an array of lines
def getLines(fileName):
    with open(fileName) as f:
        lines = f.readlines()
    return lines

def printData(players):
    for player1 in players:
        print(player1.name + " " + str(player1.games.points))
        
def parseData(line):
    parts = line.split("::")
    week9game = game.Game(parts[1], parts[2], parts[3], "placeholder")
    player1 = player.Player(parts[0], week9game)
    return player1

def readTweets(player1):
    for tweet in tweepy.Cursor(api.search, q=player1.name).items(10):
        tweetText = tweet.text.replace('\n','')
        formatted = '{}::::{}::::{}::::{}\n'.format(tweet.created_at, tweet.retweet_count, tweetText, tweet.id)
        outputFile.write(formatted)

# setup the authorization
exec(open("..\config\TwitterTokens.py").read())

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

# create output file
outputFile = open("..\output\week9_tweets.txt", "w", encoding="utf-8")

# read in the stats
#statsFile = open("..\config\week9.dat", "r", encoding="utf-8") 
week9data = getLines("..\config\week9.dat")

# get the list of fantasy football experts
ffbExperts = getLines(r"..\config\users.dat")

for expert in ffbExperts:
    print(expert)
    
players = []
# parse the data
for line in week9data:
    player1 = parseData(line)
    players.append(player1)
    readTweets(player1)
    
#printData(players)
outputFile.close()
